import os
import sys
import tempfile
import torch
import numpy as np
from PIL import Image
import cv2
import folder_paths

# Make sure we can import from the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Try absolute import
try:
    from youtube_uploader import YouTubeUploader, GOOGLE_APIS_AVAILABLE
    from config import Config
    if not GOOGLE_APIS_AVAILABLE:
        raise ImportError("Google API libraries not installed")
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Error: Cannot load YouTube uploader. {e}")
    print("Please install dependencies with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    YouTubeUploader = None
    Config = None
    DEPENDENCIES_AVAILABLE = False

class YouTubeUploaderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("IMAGE",),  # ComfyUI video as image sequence
                "title": ("STRING", {
                    "multiline": False,
                    "default": "My Awesome Short #1"
                }),
                "description": ("STRING", {
                    "multiline": True,
                    "default": "Check out this amazing video! 🔥\n\n#Shorts #YouTube #ComfyUI #AI"
                }),
                "tags": ("STRING", {
                    "multiline": False,
                    "default": "shorts,youtube,ai,comfyui,viral"
                }),
                "privacy": (["private", "unlisted", "public"], {
                    "default": "private"
                }),
                "fps": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 60,
                    "step": 1
                }),
                "upload_enabled": ("BOOLEAN", {
                    "default": False
                }),
            },
            "optional": {
                "audio": ("AUDIO",),  # Optional audio input
                "thumbnail": ("IMAGE",),  # Optional custom thumbnail
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN")
    RETURN_NAMES = ("video_id", "upload_url", "success")
    FUNCTION = "upload_to_youtube"
    CATEGORY = "YouTube/Upload"
    OUTPUT_NODE = True

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise RuntimeError("YouTube Uploader module not available. Check youtube_uploader.py file.")
        if not DEPENDENCIES_AVAILABLE:
            raise RuntimeError("YouTube Uploader dependencies not installed. Please run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        self.uploader = YouTubeUploader()
        self.config = Config()
        
    def upload_to_youtube(self, video, title, description, tags, privacy, fps, upload_enabled, audio=None, thumbnail=None):
        """Upload video to YouTube"""
        
        if not upload_enabled:
            print("⚠️ YouTube upload is disabled. Set 'upload_enabled' to True to upload.")
            return ("", "", False)
        
        try:
            # Convert image sequence to video file
            video_path = self._create_video_from_images(video, fps, audio)
              # Prepare thumbnail if provided
            thumbnail_path = None
            if thumbnail is not None:
                thumbnail_path = self._save_thumbnail(thumbnail)
            
            # Authenticate if needed
            if not self.uploader.service:
                print("🔐 Authenticating with YouTube...")
                self.uploader.authenticate()
              # Upload video
            print(f"🚀 Uploading video: {title}")
            video_id = self.uploader.upload_video(
                video_path, title, description, tags, privacy
            )
            
            if video_id:
                upload_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"✅ Upload successful! Video ID: {video_id}")
                print(f"🔗 Video URL: {upload_url}")
                
                # Set thumbnail if provided
                if thumbnail_path and video_id:
                    self._set_video_thumbnail(video_id, thumbnail_path)
                
                # Cleanup temporary files
                self._cleanup_temp_files(video_path, thumbnail_path)
                
                return (video_id, upload_url, True)
            else:
                print("❌ Upload failed")
                return ("", "", False)
                
        except Exception as e:
            print(f"❌ Error uploading to YouTube: {str(e)}")
            return ("", "", False)
    
    def _create_video_from_images(self, images, fps, audio=None):
        """Convert ComfyUI image sequence to video file"""
        if len(images.shape) == 3:
            # Single image, create 3-second video
            images = images.unsqueeze(0).repeat(fps * 3, 1, 1, 1)
        
        # Convert tensor to numpy
        if isinstance(images, torch.Tensor):
            images_np = images.cpu().numpy()
        else:
            images_np = images
        
        # Ensure values are in 0-255 range
        if images_np.max() <= 1.0:
            images_np = (images_np * 255).astype(np.uint8)
        else:
            images_np = images_np.astype(np.uint8)
        
        # Create temporary video file
        temp_dir = tempfile.gettempdir()
        video_path = os.path.join(temp_dir, f"comfyui_youtube_upload_{hash(str(images_np.shape))}.mp4")
        
        # Get video dimensions
        height, width = images_np.shape[1:3]
        
        # Ensure dimensions are even (required for some codecs)
        if width % 2 != 0:
            width -= 1
        if height % 2 != 0:
            height -= 1
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        try:
            for i in range(len(images_np)):
                frame = images_np[i]
                
                # Resize if needed
                if frame.shape[1] != width or frame.shape[0] != height:
                    frame = cv2.resize(frame, (width, height))
                
                # Convert RGB to BGR for OpenCV
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                out.write(frame)
            
            out.release()
            
            # Add audio if provided
            if audio is not None:
                video_path = self._add_audio_to_video(video_path, audio)
            
            print(f"📹 Created video: {video_path}")
            return video_path
            
        except Exception as e:
            out.release()
            print(f"❌ Error creating video: {str(e)}")
            raise
    
    def _add_audio_to_video(self, video_path, audio):
        """Add audio to video using ffmpeg"""
        try:
            import subprocess
            
            # Save audio to temporary file
            audio_path = video_path.replace('.mp4', '_audio.wav')
            
            # Convert audio tensor to wav file
            if isinstance(audio, torch.Tensor):
                audio_np = audio.cpu().numpy()
            else:
                audio_np = audio
            
            # Save audio using scipy or librosa if available
            try:
                import scipy.io.wavfile as wavfile
                # Ensure audio is in correct format
                if audio_np.max() <= 1.0:
                    audio_np = (audio_np * 32767).astype(np.int16)
                wavfile.write(audio_path, 44100, audio_np)
            except ImportError:
                print("⚠️ scipy not available, skipping audio")
                return video_path
            
            # Combine video and audio
            output_path = video_path.replace('.mp4', '_with_audio.mp4')
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Cleanup
            os.remove(video_path)
            os.remove(audio_path)
            
            return output_path
            
        except Exception as e:
            print(f"⚠️ Could not add audio: {str(e)}")
            return video_path
    
    def _save_thumbnail(self, thumbnail):
        """Save thumbnail image to temporary file"""
        if isinstance(thumbnail, torch.Tensor):
            thumbnail_np = thumbnail.cpu().numpy()
        else:
            thumbnail_np = thumbnail
        
        # Convert to PIL Image
        if thumbnail_np.max() <= 1.0:
            thumbnail_np = (thumbnail_np * 255).astype(np.uint8)
        
        if len(thumbnail_np.shape) == 4:
            thumbnail_np = thumbnail_np[0]  # Take first image if batch
        
        img = Image.fromarray(thumbnail_np)
        
        # Save to temporary file
        temp_dir = tempfile.gettempdir()
        thumbnail_path = os.path.join(temp_dir, f"comfyui_thumbnail_{hash(str(thumbnail_np.shape))}.jpg")
        img.save(thumbnail_path, 'JPEG', quality=95)
        
        return thumbnail_path
    
    def _set_video_thumbnail(self, video_id, thumbnail_path):
        """Set custom thumbnail for uploaded video"""
        try:
            # This requires additional YouTube API permissions
            self.uploader.youtube.thumbnails().set(
                videoId=video_id,
                media_body=thumbnail_path
            ).execute()
            print("🖼️ Custom thumbnail set successfully")
        except Exception as e:
            print(f"⚠️ Could not set thumbnail: {str(e)}")
    
    def _cleanup_temp_files(self, *file_paths):
        """Clean up temporary files"""
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass

class YouTubeAuthNode:
    """Separate node for YouTube authentication"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "client_id": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "client_secret": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "authenticate_now": ("BOOLEAN", {
                    "default": False
                }),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("authenticated", "channel_info")
    FUNCTION = "authenticate_youtube"
    CATEGORY = "YouTube/Auth"

    def authenticate_youtube(self, client_id, client_secret, authenticate_now):
        """Authenticate with YouTube API"""
        
        if not authenticate_now:
            return (False, "Authentication not requested")
        
        try:
            # Create uploader instance
            uploader = YouTubeUploader()
            
            # Create client secrets if provided
            if client_id and client_secret:
                config = Config()
                config.CLIENT_ID = client_id
                config.CLIENT_SECRET = client_secret
                config.PROJECT_ID = "comfyui-youtube-uploader"
                config.create_client_secrets_file()
            
            # Authenticate
            uploader.authenticate()
            
            # Get channel info
            channel_info = uploader.get_channel_info()
            if channel_info:
                info_text = f"Channel: {channel_info['title']}\nSubscribers: {channel_info['subscriber_count']}\nVideos: {channel_info['video_count']}"
            else:
                info_text = "Authentication successful"
            
            print(f"✅ YouTube authentication successful!")
            print(f"📺 {info_text}")
            
            return (True, info_text)
            
        except Exception as e:
            error_msg = f"Authentication failed: {str(e)}"
            print(f"❌ {error_msg}")
            return (False, error_msg)

# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "YouTubeUploaderNode": YouTubeUploaderNode,
    "YouTubeAuthNode": YouTubeAuthNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YouTubeUploaderNode": "🎬 YouTube Uploader",
    "YouTubeAuthNode": "🔐 YouTube Auth"
}

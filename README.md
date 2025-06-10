[Support me and buy me a coffee :)](coff.ee/chao.k)

<a href="https://www.buymeacoffee.com/chao.k"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=chao.k&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff" /></a>

Discamler: AI models have been utilized in creation of this repo.

# 🎬 YouTube Uploader Nodes for ComfyUI

Upload videos directly to YouTube from your ComfyUI workflows!

## 🚀 Features

- **Direct Upload**: Upload generated videos straight to YouTube
- **Custom Thumbnails**: Set custom thumbnails for your videos
- **Audio Support**: Include audio in your uploads
- **Safety Features**: Upload protection to prevent accidents
- **Shorts Optimized**: Perfect for vertical video workflows

## 📦 Installation

### Method 1: Copy to ComfyUI Custom Nodes

```bash
# Copy the entire comfyui_nodes folder to your ComfyUI custom_nodes directory
cp -r f:/YouTubeUploader/comfyui_nodes /path/to/ComfyUI/custom_nodes/youtube_uploader
```

### Method 2: Symbolic Link (Recommended for Development)

```bash
# Create symbolic link in ComfyUI custom_nodes
ln -s f:/YouTubeUploader/comfyui_nodes /path/to/ComfyUI/custom_nodes/youtube_uploader
```

### Install Dependencies

```bash
cd /path/to/ComfyUI
pip install -r custom_nodes/youtube_uploader/requirements_comfyui.txt
```

## 🔧 Setup

### 1. YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop application)
4. Note your Client ID and Client Secret

### 2. Node Configuration

#### YouTube Auth Node
- **Input**: Client ID, Client Secret, Authenticate Now
- **Output**: Authentication status and channel info
- **Usage**: Set up once per session

#### YouTube Uploader Node
- **Video Input**: Connect from any video generation node
- **Text Inputs**: Title, description, tags
- **Settings**: Privacy level, FPS, upload enabled
- **Optional**: Audio track, custom thumbnail

## 🎯 Workflow Examples

### Basic Video Upload
```
[Video Generation] → [YouTube Uploader] 
                     ↑
[YouTube Auth] ──────┘
```

### Advanced with Audio and Thumbnail
```
[Video Generation] → [YouTube Uploader] ← [Audio Generation]
                     ↑                    ↑
[YouTube Auth] ──────┘                    [Thumbnail Generator]
```

## ⚠️ Safety Features

### Upload Protection
- **upload_enabled**: Must be set to `True` to actually upload
- **Status Display**: Shows current upload status

### Testing Mode
1. Set `upload_enabled` to `False`
2. Test your workflow
3. Check video preview
4. Enable upload only when ready

## 🎨 Node Features

### YouTube Uploader Node
- **Smart Video Conversion**: Handles image sequences and single frames
- **Audio Integration**: Automatically combines video with audio
- **Error Handling**: Graceful failure with detailed messages

### YouTube Auth Node
- **One-Time Setup**: Authenticate once per session
- **Channel Info**: Displays connected channel details
- **Credential Management**: Secure handling of API keys

## 🔍 Troubleshooting

### Common Issues

#### Authentication Failed
- Check Client ID and Secret
- Ensure YouTube Data API v3 is enabled
- Verify OAuth consent screen is configured

#### Video Upload Failed
- Check file size (max 256MB)
- Verify video format compatibility
- Ensure stable internet connection

#### Node Not Appearing
- Restart ComfyUI after installation
- Check console for error messages
- Verify all dependencies are installed


## 🎵 Audio Support

### Supported Formats
- WAV, MP3, FLAC (via librosa)
- Raw audio tensors from ComfyUI nodes
- Auto-conversion to AAC for upload

### Audio Processing
- Automatic sample rate conversion
- Volume normalization
- Sync with video duration

## 🖼️ Thumbnail Features

### Auto-Thumbnails
- Uses first frame if no custom thumbnail
- Automatic aspect ratio correction
- Quality optimization for YouTube

### Custom Thumbnails
- Connect any image generation node
- Supports batch processing
- Auto-resize to YouTube specs

## 📊 Analytics Integration

### Upload Tracking
- Video ID capture for analytics
- Direct YouTube Studio links
- Upload timestamp logging

### Workflow Metrics
- Processing time tracking
- Success/failure rates
- File size optimization stats

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Test with multiple ComfyUI versions
4. Submit pull request

### Adding Features
- Follow ComfyUI node conventions
- Add comprehensive error handling
- Include unit tests for core functions
- Update documentation

## 🆘 Support

- GitHub Issues: Report bugs and feature requests

---

**⚠️ Important**: Always test uploads with private videos first. Respect YouTube's Terms of Service and community guidelines.

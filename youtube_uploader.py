import os
import pickle

# Check if Google API dependencies are available
try:
    from google.auth.transport.requests import Request
    from google.auth.exceptions import RefreshError
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    GOOGLE_APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google API dependencies not available: {e}")
    GOOGLE_APIS_AVAILABLE = False

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly'
]

if GOOGLE_APIS_AVAILABLE:
    class YouTubeUploader:
        def __init__(self):
            self.service = None
            self.credentials = None
        
        def authenticate(self, client_id=None, client_secret=None):
            """Authenticate with YouTube API"""
            creds = None
            
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            token_file = os.path.join(script_dir, 'token.pickle')
            
            if os.path.exists(token_file):
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except RefreshError:
                        creds = None
                
                if not creds:
                    # Try to use client secrets file first
                    client_secrets_file = os.path.join(script_dir, 'client_secret.json')
                    print(f"🔍 Looking for client secrets file: {client_secrets_file}")
                    if os.path.exists(client_secrets_file):
                        print(f"✅ Found client secrets file: {client_secrets_file}")
                        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                        creds = flow.run_local_server(port=0)
                    elif client_id and client_secret:
                        # Fall back to using provided credentials
                        print("🔑 Using provided credentials")
                        client_config = {
                            "installed": {
                                "client_id": client_id,
                                "client_secret": client_secret,
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token"
                            }
                        }
                        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                        creds = flow.run_local_server(port=0)
                    else:
                        raise Exception(f"No client secrets file found at {client_secrets_file} and no credentials provided")
                
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.credentials = creds
            self.service = build('youtube', 'v3', credentials=creds)
            return creds
        
        def upload_video(self, video_path, title, description, tags, privacy='private'):
            """Upload video to YouTube"""
            if not self.service:
                raise Exception("Not authenticated. Call authenticate() first.")
            
            # Handle tags - convert to list if it's a string, or use as-is if it's already a list
            if isinstance(tags, str):
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            elif isinstance(tags, list):
                tags_list = [str(tag).strip() for tag in tags if str(tag).strip()]
            else:
                tags_list = []
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags_list,
                    'categoryId': '22'  # People & Blogs
                },
                'status': {
                    'privacyStatus': privacy
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            try:
                request = self.service.videos().insert(
                    part=','.join(body.keys()),
                    body=body,
                    media_body=media
                )
                
                response = request.execute()
                video_id = response['id']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                return video_id, video_url, True
                
            except HttpError as e:
                print(f"An HTTP error occurred: {e}")
                return "", "", False
            except Exception as e:
                print(f"An error occurred: {e}")
                return "", "", False
        
        def _resumable_upload(self, insert_request):
            """Handle resumable upload with retry logic"""
            response = None
            error = None
            retry = 0
            
            while response is None:
                try:
                    status, response = insert_request.next_chunk()
                    if response is not None:
                        if 'id' in response:
                            return response
                        else:
                            raise Exception(f"Upload failed with unexpected response: {response}")
                except HttpError as e:
                    if e.resp.status in [500, 502, 503, 504]:
                        error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                        retry += 1
                        if retry > 3:
                            break
                    else:
                        raise
                except Exception as e:
                    error = f"An error occurred: {e}"
                    break
            
            if error:
                print(error)
            return None
        
        def get_channel_info(self):
            """Get information about the authenticated channel"""
            if not self.service:
                return None
            
            try:
                response = self.service.channels().list(
                    part='snippet,statistics',
                    mine=True
                ).execute()
                
                if response['items']:
                    channel = response['items'][0]
                    return {
                        'title': channel['snippet']['title'],
                        'subscriber_count': channel['statistics'].get('subscriberCount', 'Hidden'),
                        'video_count': channel['statistics']['videoCount']
                    }
            except Exception as e:
                print(f"Error getting channel info: {e}")
            
            return None

else:
    # Placeholder class when Google APIs are not available
    class YouTubeUploader:
        def __init__(self):
            self.service = None
            self.credentials = None
            
        def authenticate(self, client_id=None, client_secret=None):
            raise ImportError("Google API dependencies not installed")
            
        def upload_video(self, video_path, title, description, tags, privacy='private'):
            raise ImportError("Google API dependencies not installed")
            
        def get_channel_info(self):
            raise ImportError("Google API dependencies not installed")
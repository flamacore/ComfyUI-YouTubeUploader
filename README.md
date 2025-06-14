[![Buy me a Coffee](https://buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://buymeacoffee.com/chao.k)

# 🎬 ComfyUI YouTube Uploader

Upload videos directly to YouTube from your ComfyUI workflows! Perfect for AI-generated content creators.

## ✨ Features

- **Direct Upload**: Upload generated videos straight to YouTube
- **Custom Thumbnails**: Set custom thumbnails for your videos  
- **Audio Support**: Include audio in your uploads
- **Safety Features**: Upload protection to prevent accidents
- **Shorts Optimized**: Perfect for vertical video workflows
- **ComfyUI-Manager Compatible**: Easy installation and updates

## 📦 Installation

### Via ComfyUI-Manager (Recommended)

1. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
2. Search for "YouTube Uploader" in Custom Nodes
3. Click Install
4. Restart ComfyUI

### Manual Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/comfyui-youtube-uploader.git
cd comfyui-youtube-uploader
pip install -r requirements.txt
```

## 🔧 Setup

### 1. YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop application)
4. Download `client_secret.json` to the node folder OR use the Auth node

### 2. Basic Usage

1. **YouTube Auth Node**: Authenticate once per session
   - Input your Client ID and Client Secret
   - Set "Authenticate Now" to True
   - Follow browser authentication

2. **YouTube Uploader Node**: Upload your videos
   - Connect video input from any generation node
   - Set title, description, tags
   - **Important**: Set "upload_enabled" to True to actually upload
   - Choose privacy setting (private/unlisted/public)

## 🎯 Node Reference

### YouTube Auth Node 🔐
- **Inputs**: Client ID, Client Secret, Authenticate Now
- **Outputs**: Authentication status, Channel info
- **Purpose**: One-time authentication setup

### YouTube Uploader Node 🎬
- **Required Inputs**: 
  - Video (IMAGE sequence)
  - Title, Description, Tags
  - Privacy, FPS, Upload Enabled
- **Optional Inputs**: 
  - Audio (AUDIO)
  - Thumbnail (IMAGE)
- **Outputs**: Video ID, Upload URL, Success status

## ⚠️ Safety Features

- **Upload Protection**: Must explicitly enable uploads
- **Testing Mode**: Test workflows without uploading
- **Error Handling**: Graceful failure with detailed messages
- **Dependency Checks**: Works even if dependencies missing

## 🎵 Supported Formats

- **Video**: Any format ComfyUI can generate
- **Audio**: WAV, MP3, FLAC (auto-converted to AAC)
- **Thumbnails**: Any image format (auto-resized)

## 🔍 Troubleshooting

### Common Issues

**"Dependencies not available"**
```bash
cd ComfyUI/custom_nodes/comfyui-youtube-uploader
pip install -r requirements.txt
```

**Authentication Failed**
- Check Client ID/Secret are correct
- Ensure YouTube Data API v3 is enabled
- Verify OAuth consent screen is configured

**Upload Failed**
- Check file size limits (256MB max)
- Verify internet connection
- Ensure video format is compatible

## 📋 Requirements

- Python 3.8+
- ComfyUI
- Google Cloud Project with YouTube API enabled
- Internet connection for uploads

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test with ComfyUI-Manager
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- GitHub Issues: Bug reports and features
- ComfyUI Discord: Community support

---

**⚠️ Important**: Always test uploads with private videos first. Respect YouTube's Terms of Service and community guidelines.

**💡 Tip**: Use with AI video generation nodes for automated content creation workflows!

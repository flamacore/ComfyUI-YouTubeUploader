[![Buy me a Coffee](https://buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://buymeacoffee.com/chao.k)


Disclaimer: AI models have been utilized in creation of this repo and this repo is under HEAVY development. It works fine, pretty basic but still use with care please.

# 🎬 YouTube Uploader Nodes for ComfyUI

Upload videos directly to YouTube from your ComfyUI workflows!

<img width="1062" alt="ComfyUI_ow3dB7audK" src="https://github.com/user-attachments/assets/5e90807a-b777-420d-9fdc-d5fbc552ef94" />


## 🚀 Features

- **Direct Upload**: Upload generated videos straight to YouTube
- **Custom Thumbnails**: Set custom thumbnails for your videos
- **Audio Support**: Include audio in your uploads
- **Safety Features**: Upload protection to prevent accidents
- **Shorts Optimized**: Perfect for vertical video workflows

## 📦 Installation

## If ComfyUI Manager finds this repo, then the best way to install is from there. 

Otherwise;

### Method 1: Clone from GitHub (Recommended)

```bash
# Navigate to your ComfyUI custom_nodes directory
cd /path/to/ComfyUI/custom_nodes

# Clone the repository
git clone https://github.com/flamacore/ComfyUI-YouTubeUploader.git
```

**Windows (Command Prompt):**
```cmd
# Navigate to your ComfyUI custom_nodes directory
cd C:\path\to\ComfyUI\custom_nodes

# Clone the repository
git clone https://github.com/flamacore/ComfyUI-YouTubeUploader.git
```

### Method 2: Download and Extract

1. Download the repository as a ZIP file
2. Extract to your ComfyUI `custom_nodes` directory
3. Rename the folder to `ComfyUI-YouTubeUploader` if needed

### Method 3: Manual Copy (Windows)

```cmd
# Copy the entire directory to your ComfyUI custom_nodes directory
xcopy /E /I "C:\path\to\ComfyUI-YouTubeUploader" "C:\path\to\ComfyUI\custom_nodes\ComfyUI-YouTubeUploader"
```

### Install Dependencies

**Windows (Command Prompt):**
```cmd
# Navigate to the node directory
cd custom_nodes\ComfyUI-YouTubeUploader

# Install Google API dependencies
pip install -r requirements.txt

# Install ComfyUI-specific dependencies
pip install -r requirements_comfyui.txt
```

**Linux/macOS (Terminal):**
```bash
# Navigate to the node directory
cd custom_nodes/ComfyUI-YouTubeUploader

# Install Google API dependencies
pip install -r requirements.txt

# Install ComfyUI-specific dependencies
pip install -r requirements_comfyui.txt
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
- Check file size (YouTube has upload limits based on account verification status)
- Verify video format compatibility
- Ensure stable internet connection

#### Node Not Appearing
- Restart ComfyUI after installation
- Check console for error messages
- Verify all dependencies are installed

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

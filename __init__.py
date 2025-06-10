import os
import sys

# Add the current directory to path to help Python find the modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Now import the node mappings
from youtube_uploader_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# Version info
__version__ = "1.0.0"
__author__ = "ComfyUI YouTube Extension"
__description__ = "Upload videos to YouTube directly from ComfyUI workflows"

# Display loading message
print(f"🎬 YouTube Uploader Nodes v{__version__} loaded!")
print("📺 Ready to upload videos to YouTube from ComfyUI")

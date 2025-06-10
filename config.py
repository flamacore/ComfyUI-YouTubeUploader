import os
import json

class Config:
    def __init__(self):
        self.CLIENT_ID = ""
        self.CLIENT_SECRET = ""
        self.PROJECT_ID = "comfyui-youtube-uploader"
        self.CLIENT_SECRETS_FILE = "client_secret.json"
        
        # Get the directory where this config file is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.client_secrets_path = os.path.join(self.base_dir, self.CLIENT_SECRETS_FILE)
    
    def create_client_secrets_file(self):
        """Create client_secret.json file with provided credentials"""
        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("CLIENT_ID and CLIENT_SECRET must be provided")
        
        client_secrets = {
            "installed": {
                "client_id": self.CLIENT_ID,
                "project_id": self.PROJECT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": self.CLIENT_SECRET,
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open(self.client_secrets_path, 'w') as f:
            json.dump(client_secrets, f, indent=2)
        
        print(f"✅ Created client secrets file: {self.client_secrets_path}")
        return self.client_secrets_path
    
    def get_client_secrets_path(self):
        """Get the full path to client_secret.json"""
        return self.client_secrets_path
    
    def has_client_secrets(self):
        """Check if client_secret.json exists"""
        return os.path.exists(self.client_secrets_path)

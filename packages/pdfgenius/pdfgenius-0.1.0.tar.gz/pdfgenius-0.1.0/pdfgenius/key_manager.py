# pdf_extractor/key_manager.py
import json
from pathlib import Path
import os
from cryptography.fernet import Fernet


class KeyManager:
    def __init__(self):
        self.config_dir = Path.home() / ".pdf_extractor"
        self.keys_file = self.config_dir / "keys.enc"
        self.encryption_key_file = self.config_dir / ".encryption_key"
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize the storage directory and encryption key"""
        self.config_dir.mkdir(exist_ok=True)

        # Create or load encryption key
        if not self.encryption_key_file.exists():
            encryption_key = Fernet.generate_key()
            self.encryption_key_file.write_bytes(encryption_key)

        self.fernet = Fernet(self.encryption_key_file.read_bytes())

        # Create empty keys file if it doesn't exist
        if not self.keys_file.exists():
            self._save_keys({})

    def _load_keys(self):
        """Load and decrypt keys"""
        if not self.keys_file.exists():
            return {}
        encrypted_data = self.keys_file.read_bytes()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)

    def _save_keys(self, keys):
        """Encrypt and save keys"""
        encrypted_data = self.fernet.encrypt(json.dumps(keys).encode())
        self.keys_file.write_bytes(encrypted_data)

    def add_key(self, model: str, api_key: str):
        """Add a new API key"""
        keys = self._load_keys()
        keys[model.lower()] = api_key
        self._save_keys(keys)

    def get_key(self, model: str) -> str:
        """Get API key for a model"""
        keys = self._load_keys()
        return keys.get(model.lower())

    def delete_key(self, model: str):
        """Delete API key for a model"""
        keys = self._load_keys()
        if model.lower() in keys:
            del keys[model.lower()]
            self._save_keys(keys)

    def list_keys(self):
        """List all stored models with partial key preview"""
        keys = self._load_keys()
        preview = {}
        for model, key in keys.items():
            # Show only first 4 and last 4 characters
            preview[model] = f"{key[:4]}...{key[-4:]}"
        return preview

import os
import json

class Settings:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
        
    def initialize(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.filepath = os.path.join(self.data_dir, "settings.json")
        
        self.default_settings = {
            "theme": "dark",
            "currency": "USD",
            "animations_enabled": True
        }
        self.settings = self.load()
        
    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return {**self.default_settings, **json.load(f)}
            except Exception:
                pass
        return self.default_settings.copy()
        
    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")
            
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
        
    def set(self, key, value):
        self.settings[key] = value
        self.save()


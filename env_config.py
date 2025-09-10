#!/usr/bin/env python3
"""
Environment configuration loader for Azure Cognitive Search Manager
Loads configuration from .env file and environment variables
"""

import os
from typing import Optional, Union
from pathlib import Path

def load_env_file(env_path: str = ".env") -> None:
    """Load environment variables from .env file"""
    env_file = Path(env_path)
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key.strip()] = value
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print(f"⚠️  Environment file {env_path} not found, using system environment variables")

def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """Get environment variable with optional default value"""
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

def get_bool_env(key: str, default: bool = False) -> bool:
    """Get boolean environment variable"""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')

def get_int_env(key: str, default: int = 0) -> int:
    """Get integer environment variable"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_list_env(key: str, default: Optional[list] = None, separator: str = ',') -> list:
    """Get list environment variable (comma-separated)"""
    value = os.getenv(key)
    if value is None:
        return default or []
    return [item.strip() for item in value.split(separator) if item.strip()]

class EnvironmentConfig:
    """Environment configuration class"""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment"""
        load_env_file(env_file)
        self._load_config()
    
    def _load_config(self):
        """Load all configuration values"""
        # Application settings
        self.APP_NAME = get_env_var("APP_NAME", "Azure Cognitive Search Manager")
        self.APP_VERSION = get_env_var("APP_VERSION", "1.0.0")
        self.DEBUG = get_bool_env("DEBUG", True)
        self.ENVIRONMENT = get_env_var("ENVIRONMENT", "development")
        
        # Server configuration
        self.HOST = get_env_var("HOST", "0.0.0.0")
        self.PORT = get_int_env("PORT", 8000)
        self.RELOAD = get_bool_env("RELOAD", True)
        
        # File paths
        self.CONFIG_DIR = get_env_var("CONFIG_DIR", "azure_configs")
        self.INDEX_FILE_PATH = get_env_var("INDEX_FILE_PATH", os.path.join(self.CONFIG_DIR, "search_index.json"))
        self.SKILLSET_FILE_PATH = get_env_var("SKILLSET_FILE_PATH", os.path.join(self.CONFIG_DIR, "search_skillset.json"))
        self.BACKUP_DIR = get_env_var("BACKUP_DIR", os.path.join(self.CONFIG_DIR, "backups"))
        
        # Azure settings (optional)
        self.AZURE_SEARCH_SERVICE_NAME = get_env_var("AZURE_SEARCH_SERVICE_NAME")
        self.AZURE_SEARCH_ADMIN_KEY = get_env_var("AZURE_SEARCH_ADMIN_KEY")
        self.AZURE_SEARCH_QUERY_KEY = get_env_var("AZURE_SEARCH_QUERY_KEY")
        self.AZURE_SEARCH_INDEX_NAME = get_env_var("AZURE_SEARCH_INDEX_NAME")
        self.AZURE_SEARCH_SKILLSET_NAME = get_env_var("AZURE_SEARCH_SKILLSET_NAME")
        
        # Logging
        self.LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO")
        self.LOG_FILE = get_env_var("LOG_FILE", "logs/azure_search_manager.log")
        self.LOG_MAX_SIZE = get_env_var("LOG_MAX_SIZE", "10MB")
        self.LOG_BACKUP_COUNT = get_int_env("LOG_BACKUP_COUNT", 5)
        
        # Security
        self.SECRET_KEY = get_env_var("SECRET_KEY", "your-secret-key-change-this-in-production")
        self.ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1", "0.0.0.0"])
        self.CORS_ORIGINS = get_list_env("CORS_ORIGINS", ["http://localhost:3000", "http://localhost:8000"])
        
        # Feature flags
        self.AUTO_CREATE_SAMPLE_FILES = get_bool_env("AUTO_CREATE_SAMPLE_FILES", True)
        self.BACKUP_BEFORE_OVERWRITE = get_bool_env("BACKUP_BEFORE_OVERWRITE", True)
        self.ENABLE_API_DOCS = get_bool_env("ENABLE_API_DOCS", True)
        self.ENABLE_METRICS = get_bool_env("ENABLE_METRICS", True)
        
        # Development settings
        self.DEV_MODE = get_bool_env("DEV_MODE", True)
        self.HOT_RELOAD = get_bool_env("HOT_RELOAD", True)
        self.VERBOSE_LOGGING = get_bool_env("VERBOSE_LOGGING", True)
        
        # Testing
        self.TEST_CONFIG_DIR = get_env_var("TEST_CONFIG_DIR", "test_configs")
        self.TEST_INDEX_FILE = get_env_var("TEST_INDEX_FILE", os.path.join(self.TEST_CONFIG_DIR, "test_index.json"))
        self.TEST_SKILLSET_FILE = get_env_var("TEST_SKILLSET_FILE", os.path.join(self.TEST_CONFIG_DIR, "test_skillset.json"))
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [self.CONFIG_DIR]
        if self.BACKUP_BEFORE_OVERWRITE:
            directories.append(self.BACKUP_DIR)
        if self.ENVIRONMENT == "development":
            directories.append("logs")
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Directory created/verified: {directory}")
    
    def get_config_info(self) -> dict:
        """Get current configuration information"""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "environment": self.ENVIRONMENT,
            "debug": self.DEBUG,
            "host": self.HOST,
            "port": self.PORT,
            "config_directory": self.CONFIG_DIR,
            "index_file_path": self.INDEX_FILE_PATH,
            "skillset_file_path": self.SKILLSET_FILE_PATH,
            "backup_directory": self.BACKUP_DIR,
            "auto_create_samples": self.AUTO_CREATE_SAMPLE_FILES,
            "azure_configured": bool(self.AZURE_SEARCH_SERVICE_NAME),
            "dev_mode": self.DEV_MODE
        }
    
    def print_config(self):
        """Print current configuration"""
        print("🔧 Azure Cognitive Search Manager - Configuration")
        print("=" * 50)
        info = self.get_config_info()
        for key, value in info.items():
            print(f"{key}: {value}")

# Global configuration instance
config = EnvironmentConfig()

if __name__ == "__main__":
    config.print_config()
    config.create_directories()
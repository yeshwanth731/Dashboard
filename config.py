#!/usr/bin/env python3
"""
Configuration file for Azure Cognitive Search Manager
Modify these settings to customize file paths and behavior
"""

import os

# =============================================================================
# FILE PATH CONFIGURATION
# =============================================================================

# Base directory for storing configuration files
CONFIG_DIR = "azure_configs"

# Specific file paths for JSON configurations
INDEX_FILE_PATH = os.path.join(CONFIG_DIR, "search_index.json")
SKILLSET_FILE_PATH = os.path.join(CONFIG_DIR, "search_skillset.json")

# Alternative file path examples (uncomment to use):
# INDEX_FILE_PATH = "/home/user/azure-configs/my_index.json"
# SKILLSET_FILE_PATH = "/home/user/azure-configs/my_skillset.json"

# Or use absolute paths:
# INDEX_FILE_PATH = "/var/lib/azure-search/index.json"
# SKILLSET_FILE_PATH = "/var/lib/azure-search/skillset.json"

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Server settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# File settings
AUTO_CREATE_SAMPLE_FILES = True
BACKUP_BEFORE_OVERWRITE = True
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")

# =============================================================================
# VALIDATION SETTINGS
# =============================================================================

# Required fields for index configuration
REQUIRED_INDEX_FIELDS = ["name", "fields"]
REQUIRED_FIELD_PROPERTIES = ["name", "type"]

# Required fields for skillset configuration
REQUIRED_SKILLSET_FIELDS = ["name", "description", "skills"]
REQUIRED_SKILL_PROPERTIES = ["name", "description", "context", "type"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_config_info():
    """Get current configuration information"""
    return {
        "config_directory": CONFIG_DIR,
        "index_file_path": INDEX_FILE_PATH,
        "skillset_file_path": SKILLSET_FILE_PATH,
        "index_file_exists": os.path.exists(INDEX_FILE_PATH),
        "skillset_file_exists": os.path.exists(SKILLSET_FILE_PATH),
        "backup_directory": BACKUP_DIR,
        "auto_create_samples": AUTO_CREATE_SAMPLE_FILES
    }

def create_directories():
    """Create necessary directories"""
    directories = [CONFIG_DIR]
    if BACKUP_BEFORE_OVERWRITE:
        directories.append(BACKUP_DIR)
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def validate_file_paths():
    """Validate that file paths are properly configured"""
    issues = []
    
    if not INDEX_FILE_PATH.endswith('.json'):
        issues.append("Index file path must end with .json")
    
    if not SKILLSET_FILE_PATH.endswith('.json'):
        issues.append("Skillset file path must end with .json")
    
    if not os.path.isabs(INDEX_FILE_PATH) and not os.path.isabs(SKILLSET_FILE_PATH):
        # Both are relative paths, check if they're in the same directory
        if os.path.dirname(INDEX_FILE_PATH) != os.path.dirname(SKILLSET_FILE_PATH):
            issues.append("Both file paths should be in the same directory")
    
    return issues

if __name__ == "__main__":
    print("🔧 Azure Cognitive Search Manager - Configuration")
    print("=" * 50)
    
    # Show current configuration
    info = get_config_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Validate configuration
    issues = validate_file_paths()
    if issues:
        print("\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Configuration is valid")
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
#!/usr/bin/env python3
"""
Development setup script for Azure Cognitive Search Manager
Sets up the development environment with all necessary configurations
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "azure_configs",
        "azure_configs/backups",
        "logs",
        "test_configs",
        "static/css",
        "static/js",
        "static/images",
        "templates",
        ".vscode",
        ".idea/runConfigurations"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Set up environment configuration"""
    print_header("Setting up Environment Configuration")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ Created .env from .env.example")
        else:
            print("⚠️  .env.example not found, using default configuration")
    else:
        print("✅ .env file already exists")
    
    # Test environment configuration
    try:
        from env_config import config
        config.print_config()
        print("✅ Environment configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading environment configuration: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    # Try to install dependencies
    success = run_command(
        "pip3 install -r requirements.txt",
        "Installing Python dependencies"
    )
    
    if not success:
        # Try with --break-system-packages if needed
        print("🔄 Trying with --break-system-packages flag...")
        success = run_command(
            "pip3 install -r requirements.txt --break-system-packages",
            "Installing Python dependencies (with --break-system-packages)"
        )
    
    return success

def create_virtual_environment():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    success = run_command(
        "python3 -m venv venv",
        "Creating virtual environment"
    )
    
    if success:
        print("✅ Virtual environment created")
        print("💡 To activate: source venv/bin/activate")
        print("💡 To deactivate: deactivate")
    
    return success

def test_installation():
    """Test the installation"""
    print_header("Testing Installation")
    
    # Test environment configuration
    try:
        from env_config import config
        print("✅ Environment configuration works")
    except Exception as e:
        print(f"❌ Environment configuration failed: {e}")
        return False
    
    # Test main application import
    try:
        import azure_search_manager
        print("✅ Main application imports successfully")
    except Exception as e:
        print(f"❌ Main application import failed: {e}")
        return False
    
    # Test JSON file creation
    try:
        from test_json_files import test_configuration
        if test_configuration():
            print("✅ JSON file configuration works")
        else:
            print("❌ JSON file configuration failed")
            return False
    except Exception as e:
        print(f"❌ JSON file test failed: {e}")
        return False
    
    return True

def create_ide_configs():
    """Create IDE configuration files"""
    print_header("Setting up IDE Configurations")
    
    # VS Code settings
    vscode_settings = {
        "python.defaultInterpreterPath": "./venv/bin/python",
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.formatting.provider": "black",
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/.pytest_cache": True,
            "**/venv": True
        }
    }
    
    # Create .vscode/settings.json if it doesn't exist
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    if not settings_file.exists():
        import json
        with open(settings_file, 'w') as f:
            json.dump(vscode_settings, f, indent=2)
        print("✅ VS Code settings created")
    else:
        print("✅ VS Code settings already exist")
    
    print("✅ IDE configurations ready")

def print_next_steps():
    """Print next steps for the user"""
    print_header("Next Steps")
    
    print("🚀 Your development environment is ready!")
    print("\n📋 To get started:")
    print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the application: python3 azure_search_manager.py")
    print("3. Open browser: http://localhost:8000")
    print("4. Check API docs: http://localhost:8000/docs")
    
    print("\n🔧 Development commands:")
    print("• Test configuration: python3 test_json_files.py")
    print("• Test static files: python3 test_static.py")
    print("• Run all tests: python3 -m pytest")
    print("• Format code: black --line-length 88 .")
    print("• Lint code: flake8 --max-line-length 88 .")
    
    print("\n📁 Project structure:")
    print("• Configuration: .env, config.py, env_config.py")
    print("• Main app: azure_search_manager.py")
    print("• Static files: static/")
    print("• JSON configs: azure_configs/")
    print("• IDE configs: .vscode/, .idea/")
    
    print("\n🎯 IDE Setup:")
    print("• VS Code: Install recommended extensions")
    print("• PyCharm: Import project and configure Python interpreter")
    print("• Both: Use provided run configurations")

def main():
    """Main setup function"""
    print("🚀 Azure Cognitive Search Manager - Development Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating virtual environment", create_virtual_environment),
        ("Testing installation", test_installation),
        ("Setting up IDE configs", create_ide_configs)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print(f"⚠️  {step_name} completed with warnings")
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
    
    print_header("Setup Summary")
    print(f"✅ Completed: {success_count}/{len(steps)} steps")
    
    if success_count == len(steps):
        print("🎉 Setup completed successfully!")
        print_next_steps()
    else:
        print("⚠️  Setup completed with some issues")
        print("Please check the errors above and run setup again if needed")

if __name__ == "__main__":
    main()
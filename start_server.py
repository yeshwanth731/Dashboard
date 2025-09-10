#!/usr/bin/env python3
"""
Startup script for Azure Cognitive Search Manager
"""

import os
import sys
import subprocess
import time

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import jinja2
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "azure_configs",
        "static/css",
        "static/js",
        "static/images",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def show_project_structure():
    """Display project structure"""
    print("\n📁 Project Structure:")
    print("├── azure_search_manager.py    # Main FastAPI application")
    print("├── start_server.py            # This startup script")
    print("├── run.py                     # Alternative startup script")
    print("├── test_static.py             # Test script")
    print("├── requirements.txt           # Python dependencies")
    print("├── README.md                  # Documentation")
    print("├── NON_TECHNICAL_AUTOMATION.md # Automation suggestions")
    print("├── static/                    # Static files")
    print("│   ├── index.html             # Main HTML page")
    print("│   ├── css/")
    print("│   │   └── style.css          # Custom styles")
    print("│   └── js/")
    print("│       └── main.js            # JavaScript functionality")
    print("├── templates/                 # Jinja2 templates (legacy)")
    print("│   ├── dashboard.html")
    print("│   └── error.html")
    print("└── azure_configs/             # Configuration storage")
    print("    ├── search_index.json      # Index configuration")
    print("    └── search_skillset.json   # Skillset configuration")

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Azure Cognitive Search Manager...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📍 API documentation at: http://localhost:8000/docs")
    print("📍 Press Ctrl+C to stop the server")
    print("\n" + "="*50)
    
    try:
        subprocess.run([sys.executable, "azure_search_manager.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🔧 Azure Cognitive Search Manager - Setup & Start")
    print("="*50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Show project structure
    show_project_structure()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
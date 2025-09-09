#!/usr/bin/env python3
"""
Azure Cognitive Search Configuration Manager
Run this script to start the web application
"""

import uvicorn
from azure_search_manager import app

if __name__ == "__main__":
    print("Starting Azure Cognitive Search Configuration Manager...")
    print("Access the web interface at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=True
    )
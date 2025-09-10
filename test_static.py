#!/usr/bin/env python3
"""
Test script to verify static file serving
"""

import requests
import json

def test_static_files():
    base_url = "http://localhost:8000"
    
    print("Testing static file serving...")
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            if "Azure Cognitive Search Manager" in response.text:
                print("✅ HTML content is correct")
            else:
                print("❌ HTML content is incorrect")
        else:
            print(f"❌ Main page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error loading main page: {e}")
    
    # Test CSS file
    try:
        response = requests.get(f"{base_url}/static/css/style.css")
        if response.status_code == 200:
            print("✅ CSS file loads successfully")
        else:
            print(f"❌ CSS file failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error loading CSS: {e}")
    
    # Test JS file
    try:
        response = requests.get(f"{base_url}/static/js/main.js")
        if response.status_code == 200:
            print("✅ JavaScript file loads successfully")
        else:
            print(f"❌ JavaScript file failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error loading JavaScript: {e}")
    
    # Test API endpoints
    try:
        response = requests.get(f"{base_url}/api/index")
        if response.status_code == 200:
            print("✅ Index API works")
        else:
            print(f"❌ Index API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing Index API: {e}")
    
    try:
        response = requests.get(f"{base_url}/api/skillset")
        if response.status_code == 200:
            print("✅ Skillset API works")
        else:
            print(f"❌ Skillset API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing Skillset API: {e}")

if __name__ == "__main__":
    test_static_files()
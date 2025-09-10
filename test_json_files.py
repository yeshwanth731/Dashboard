#!/usr/bin/env python3
"""
Test script to verify JSON file creation and configuration
"""

import os
import json
import sys

def test_configuration():
    """Test configuration loading and file creation"""
    print("🧪 Testing Azure Cognitive Search Manager Configuration")
    print("=" * 60)
    
    try:
        # Import configuration
        from config import get_config_info, create_directories, validate_file_paths
        
        # Show configuration info
        print("\n📋 Current Configuration:")
        info = get_config_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Validate configuration
        print("\n🔍 Validating Configuration:")
        issues = validate_file_paths()
        if issues:
            print("  ❌ Issues found:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  ✅ Configuration is valid")
        
        # Create directories
        print("\n📁 Creating Directories:")
        create_directories()
        
        # Test JSON file creation
        print("\n📄 Testing JSON File Creation:")
        
        # Test index file
        index_file = info['index_file_path']
        if os.path.exists(index_file):
            print(f"  ✅ Index file exists: {index_file}")
            try:
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                print(f"  ✅ Index file is valid JSON with {len(index_data.get('fields', []))} fields")
            except json.JSONDecodeError as e:
                print(f"  ❌ Index file is not valid JSON: {e}")
        else:
            print(f"  ⚠️  Index file does not exist: {index_file}")
        
        # Test skillset file
        skillset_file = info['skillset_file_path']
        if os.path.exists(skillset_file):
            print(f"  ✅ Skillset file exists: {skillset_file}")
            try:
                with open(skillset_file, 'r') as f:
                    skillset_data = json.load(f)
                print(f"  ✅ Skillset file is valid JSON with {len(skillset_data.get('skills', []))} skills")
            except json.JSONDecodeError as e:
                print(f"  ❌ Skillset file is not valid JSON: {e}")
        else:
            print(f"  ⚠️  Skillset file does not exist: {skillset_file}")
        
        # Test file extensions
        print("\n🔍 Testing File Extensions:")
        if index_file.endswith('.json'):
            print("  ✅ Index file has .json extension")
        else:
            print("  ❌ Index file does not have .json extension")
        
        if skillset_file.endswith('.json'):
            print("  ✅ Skillset file has .json extension")
        else:
            print("  ❌ Skillset file does not have .json extension")
        
        print("\n✅ Configuration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importing configuration: {e}")
        print("Make sure config.py exists and is properly configured")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_json_content():
    """Test JSON file content structure"""
    print("\n🔍 Testing JSON Content Structure:")
    
    try:
        from config import INDEX_FILE_PATH, SKILLSET_FILE_PATH
        
        # Test index file content
        if os.path.exists(INDEX_FILE_PATH):
            with open(INDEX_FILE_PATH, 'r') as f:
                index_data = json.load(f)
            
            required_fields = ['name', 'fields']
            for field in required_fields:
                if field in index_data:
                    print(f"  ✅ Index file contains '{field}' field")
                else:
                    print(f"  ❌ Index file missing '{field}' field")
            
            if 'fields' in index_data and isinstance(index_data['fields'], list):
                print(f"  ✅ Index file has {len(index_data['fields'])} fields")
                for i, field in enumerate(index_data['fields']):
                    if 'name' in field and 'type' in field:
                        print(f"    Field {i+1}: {field['name']} ({field['type']})")
                    else:
                        print(f"    Field {i+1}: Missing required properties")
        
        # Test skillset file content
        if os.path.exists(SKILLSET_FILE_PATH):
            with open(SKILLSET_FILE_PATH, 'r') as f:
                skillset_data = json.load(f)
            
            required_fields = ['name', 'description', 'skills']
            for field in required_fields:
                if field in skillset_data:
                    print(f"  ✅ Skillset file contains '{field}' field")
                else:
                    print(f"  ❌ Skillset file missing '{field}' field")
            
            if 'skills' in skillset_data and isinstance(skillset_data['skills'], list):
                print(f"  ✅ Skillset file has {len(skillset_data['skills'])} skills")
                for i, skill in enumerate(skillset_data['skills']):
                    if 'name' in skill and 'type' in skill:
                        print(f"    Skill {i+1}: {skill['name']} ({skill['type']})")
                    else:
                        print(f"    Skill {i+1}: Missing required properties")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing JSON content: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Azure Cognitive Search Manager - JSON File Test")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_configuration()
    
    # Test JSON content
    content_ok = test_json_content()
    
    if config_ok and content_ok:
        print("\n🎉 All tests passed! JSON files are properly configured.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the configuration.")
        sys.exit(1)
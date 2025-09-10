# JSON File Configuration Guide

## 📁 File Path Configuration

Your Azure Cognitive Search Manager now supports configurable JSON file paths. The files are automatically saved with `.json` extension and contain proper JSON content.

### 🔧 Configuration Methods

#### Method 1: Using config.py (Recommended)

Create or modify `config.py` to set your file paths:

```python
# config.py
import os

# Basic configuration
CONFIG_DIR = "azure_configs"
INDEX_FILE_PATH = os.path.join(CONFIG_DIR, "search_index.json")
SKILLSET_FILE_PATH = os.path.join(CONFIG_DIR, "search_skillset.json")

# Custom paths (examples)
# INDEX_FILE_PATH = "/home/user/my-azure-configs/index.json"
# SKILLSET_FILE_PATH = "/home/user/my-azure-configs/skillset.json"

# Absolute paths
# INDEX_FILE_PATH = "/var/lib/azure-search/index.json"
# SKILLSET_FILE_PATH = "/var/lib/azure-search/skillset.json"
```

#### Method 2: Direct modification in azure_search_manager.py

Edit the configuration section in `azure_search_manager.py`:

```python
# In azure_search_manager.py
CONFIG_DIR = "your_custom_directory"
INDEX_FILE_PATH = os.path.join(CONFIG_DIR, "your_index.json")
SKILLSET_FILE_PATH = os.path.join(CONFIG_DIR, "your_skillset.json")
```

### 📄 File Structure

The JSON files are automatically created with proper structure:

#### Index File (`search_index.json`)
```json
{
  "name": "default-index",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "searchable": false,
      "filterable": false,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "content",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "sortable": false,
      "facetable": false
    }
  ],
  "scoringProfiles": [],
  "suggesters": [],
  "analyzers": [],
  "tokenizers": [],
  "tokenFilters": [],
  "charFilters": []
}
```

#### Skillset File (`search_skillset.json`)
```json
{
  "name": "default-skillset",
  "description": "Default skillset for content processing",
  "skills": [
    {
      "name": "text-split",
      "description": "Split text into chunks",
      "context": "/document/content",
      "inputs": [
        {
          "name": "text",
          "source": "/document/content"
        }
      ],
      "outputs": [
        {
          "name": "textItems",
          "targetName": "textItems"
        }
      ],
      "type": "Microsoft.Skills.Text.SplitSkill"
    }
  ],
  "cognitiveServices": null
}
```

### 🚀 How to Use

#### 1. Start the Application
```bash
# The application will automatically create JSON files
python3 azure_search_manager.py
```

#### 2. Check File Paths
Visit `http://localhost:8000/api/config/paths` to see current file paths:

```json
{
  "config_directory": "azure_configs",
  "index_file_path": "azure_configs/search_index.json",
  "skillset_file_path": "azure_configs/search_skillset.json",
  "index_file_exists": true,
  "skillset_file_exists": true
}
```

#### 3. Upload Custom JSON Files
- Use the web interface to upload your own JSON files
- Files must have `.json` extension
- Content must be valid JSON
- The system will automatically detect if it's an index or skillset based on content

### 🔍 File Detection Logic

The system automatically detects file types based on:

1. **Filename patterns:**
   - Files containing "index" or "search" → Index configuration
   - Files containing "skill" → Skillset configuration

2. **Content structure:**
   - JSON containing "fields" array → Index configuration
   - JSON containing "skills" array → Skillset configuration

### 📋 Configuration Options

#### In config.py:
```python
# File paths
CONFIG_DIR = "azure_configs"
INDEX_FILE_PATH = os.path.join(CONFIG_DIR, "search_index.json")
SKILLSET_FILE_PATH = os.path.join(CONFIG_DIR, "search_skillset.json")

# Application settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# File management
AUTO_CREATE_SAMPLE_FILES = True
BACKUP_BEFORE_OVERWRITE = True
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")
```

### 🛠️ API Endpoints

#### Get Configuration Paths
```bash
GET /api/config/paths
```

#### Download Configuration Files
```bash
GET /api/download/index      # Downloads search_index.json
GET /api/download/skillset   # Downloads search_skillset.json
```

#### Upload Configuration Files
```bash
POST /api/upload
Content-Type: multipart/form-data
file: [JSON file]
```

### 🧪 Testing Configuration

Run the test script to verify your configuration:

```bash
python3 test_json_files.py
```

This will:
- ✅ Validate file paths
- ✅ Check file extensions
- ✅ Verify JSON structure
- ✅ Test file creation
- ✅ Show current configuration

### 📁 Example Directory Structure

```
/workspace/
├── azure_search_manager.py    # Main application
├── config.py                  # Configuration file
├── test_json_files.py         # Test script
├── azure_configs/             # Configuration directory
│   ├── search_index.json      # Index configuration
│   ├── search_skillset.json   # Skillset configuration
│   └── backups/               # Backup directory
└── static/                    # Web interface files
    ├── index.html
    ├── css/style.css
    └── js/main.js
```

### 🔒 Security Considerations

- Files are saved with proper permissions
- JSON validation prevents malformed data
- File uploads are validated for JSON format
- Backup functionality prevents data loss

### 🐛 Troubleshooting

#### Files Not Created
- Check directory permissions
- Verify CONFIG_DIR path exists
- Run test script to diagnose issues

#### Invalid JSON
- Use a JSON validator to check your files
- Ensure proper JSON syntax
- Check for trailing commas or missing quotes

#### File Path Issues
- Use absolute paths for clarity
- Ensure directories exist
- Check file permissions

### 📝 Customization Examples

#### Custom Directory Structure
```python
# config.py
CONFIG_DIR = "/var/lib/azure-search"
INDEX_FILE_PATH = "/var/lib/azure-search/production/index.json"
SKILLSET_FILE_PATH = "/var/lib/azure-search/production/skillset.json"
```

#### Environment-Specific Paths
```python
# config.py
import os

ENV = os.getenv('ENVIRONMENT', 'development')
CONFIG_DIR = f"configs/{ENV}"
INDEX_FILE_PATH = os.path.join(CONFIG_DIR, f"{ENV}_index.json")
SKILLSET_FILE_PATH = os.path.join(CONFIG_DIR, f"{ENV}_skillset.json")
```

This configuration system ensures your JSON files are properly managed with the correct extensions and content structure, while providing flexibility in file location and naming.
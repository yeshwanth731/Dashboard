# Development Environment Setup Guide

## 🚀 Quick Start

### Automated Setup
```bash
# Run the automated setup script
python3 setup_dev.py
```

### Manual Setup
```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your settings

# 3. Run the application
python3 azure_search_manager.py
```

## 📁 Project Structure

```
/workspace/
├── .env                     # Environment variables (create from .env.example)
├── .env.example            # Environment template
├── .vscode/                # VS Code configuration
│   ├── settings.json       # Editor settings
│   ├── launch.json         # Debug configurations
│   ├── tasks.json          # Build tasks
│   └── extensions.json     # Recommended extensions
├── .idea/                  # PyCharm configuration
│   ├── azure_search_manager.iml
│   └── runConfigurations/
├── azure_search_manager.py # Main FastAPI application
├── env_config.py           # Environment configuration loader
├── config.py               # Legacy configuration (optional)
├── setup_dev.py            # Development setup script
├── test_json_files.py      # JSON configuration tests
├── test_static.py          # Static file tests
├── requirements.txt        # Python dependencies
├── azure_configs/          # JSON configuration files
│   ├── search_index.json
│   ├── search_skillset.json
│   └── backups/
├── static/                 # Static web files
│   ├── index.html
│   ├── css/style.css
│   └── js/main.js
└── templates/              # Jinja2 templates (legacy)
    ├── dashboard.html
    └── error.html
```

## 🔧 Environment Configuration

### Environment Variables (.env file)

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```bash
# Application settings
APP_NAME=Azure Cognitive Search Manager
DEBUG=True
ENVIRONMENT=development

# Server configuration
HOST=0.0.0.0
PORT=8000

# File paths
CONFIG_DIR=azure_configs
INDEX_FILE_PATH=azure_configs/search_index.json
SKILLSET_FILE_PATH=azure_configs/search_skillset.json

# Azure settings (optional)
AZURE_SEARCH_SERVICE_NAME=your-service
AZURE_SEARCH_ADMIN_KEY=your-key

# Feature flags
AUTO_CREATE_SAMPLE_FILES=True
BACKUP_BEFORE_OVERWRITE=True
```

### Configuration Loading

The application loads configuration in this order:
1. `.env` file
2. System environment variables
3. Default values

## 🛠️ IDE Setup

### VS Code

#### Prerequisites
- Python extension
- Pylance extension
- Black Formatter extension
- Flake8 extension

#### Configuration
The `.vscode/` directory contains:
- `settings.json` - Editor settings and Python configuration
- `launch.json` - Debug configurations
- `tasks.json` - Build and test tasks
- `extensions.json` - Recommended extensions

#### Debug Configurations
- **Azure Search Manager - Development**: Run with development settings
- **Azure Search Manager - Production**: Run with production settings
- **Test JSON Files**: Run JSON configuration tests
- **Test Static Files**: Run static file tests

#### Tasks
- **Install Dependencies**: Install Python packages
- **Run Server**: Start the FastAPI server
- **Run Tests**: Execute test suite
- **Format Code**: Format with Black
- **Lint Code**: Check with Flake8

### PyCharm

#### Prerequisites
- Python 3.8+ interpreter
- FastAPI plugin (optional)

#### Configuration
The `.idea/` directory contains:
- `azure_search_manager.iml` - Project module file
- `runConfigurations/` - Run configurations

#### Run Configurations
- **Azure Search Manager - Development**: Development server
- **Test JSON Files**: JSON configuration tests

## 🐍 Python Environment

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

### Dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn jinja2 python-multipart pydantic
```

## 🚀 Running the Application

### Development Mode
```bash
# Using Python directly
python3 azure_search_manager.py

# Using uvicorn with reload
uvicorn azure_search_manager:app --reload --host 0.0.0.0 --port 8000

# Using the setup script
python3 setup_dev.py
```

### Production Mode
```bash
# Set environment
export ENVIRONMENT=production
export DEBUG=False

# Run application
python3 azure_search_manager.py
```

## 🧪 Testing

### Run All Tests
```bash
# JSON configuration tests
python3 test_json_files.py

# Static file tests
python3 test_static.py

# Using pytest (if installed)
pytest
```

### Test Configuration
```bash
# Test environment configuration
python3 env_config.py

# Test JSON file creation
python3 test_json_files.py
```

## 🔍 Debugging

### VS Code Debugging
1. Set breakpoints in your code
2. Press F5 or use "Run and Debug" panel
3. Select "Azure Search Manager - Development"
4. Debug session will start

### PyCharm Debugging
1. Set breakpoints in your code
2. Right-click on `azure_search_manager.py`
3. Select "Debug 'azure_search_manager'"
4. Debug session will start

### Logging
The application supports different log levels:
- `DEBUG`: Detailed information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages

Set `LOG_LEVEL` in `.env` file.

## 📝 Code Quality

### Formatting
```bash
# Format with Black
black --line-length 88 .

# Format with autopep8
autopep8 --in-place --recursive .
```

### Linting
```bash
# Lint with Flake8
flake8 --max-line-length 88 .

# Lint with Pylint
pylint azure_search_manager.py
```

### Type Checking
```bash
# Type check with mypy
mypy azure_search_manager.py
```

## 🔧 Development Tools

### Hot Reload
The application supports hot reload in development mode:
```bash
# Enable hot reload
export RELOAD=True
python3 azure_search_manager.py
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Configuration API
- **Get config paths**: `GET /api/config/paths`
- **Get index config**: `GET /api/index`
- **Get skillset config**: `GET /api/skillset`

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Install missing dependencies
pip install -r requirements.txt
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8001
python3 azure_search_manager.py
```

#### Permission Errors
```bash
# Make scripts executable
chmod +x *.py

# Check file permissions
ls -la
```

#### Environment Variables Not Loading
```bash
# Check .env file exists
ls -la .env

# Check environment variables
python3 -c "import os; print(os.getenv('DEBUG'))"
```

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export DEBUG=True
export VERBOSE_LOGGING=True
python3 azure_search_manager.py
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Cognitive Search Documentation](https://docs.microsoft.com/en-us/azure/search/)
- [Python Environment Variables](https://docs.python.org/3/library/os.html#os.environ)

### IDE Extensions
- **VS Code**: Python, Pylance, Black Formatter, Flake8
- **PyCharm**: Python, FastAPI, Database Tools

### Useful Commands
```bash
# Check Python version
python3 --version

# Check installed packages
pip list

# Check environment variables
env | grep -E "(DEBUG|PORT|HOST)"

# Check file permissions
ls -la *.py

# Check if port is available
netstat -tulpn | grep :8000
```

This development setup provides a complete environment for developing and debugging the Azure Cognitive Search Manager application with proper IDE integration and debugging capabilities.
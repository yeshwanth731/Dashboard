# Azure Cognitive Search Configuration Manager

A simple web application built with FastAPI to manage Azure Cognitive Search index and skillset JSON configuration files.

## Features

- **Web-based UI**: Simple, intuitive interface for managing configurations
- **Index Management**: Add, remove, and modify search index fields
- **Skillset Management**: Add, remove, and modify skillset skills
- **JSON Validation**: Built-in validation for Azure Cognitive Search schemas
- **File Operations**: Upload and download configuration files
- **Real-time Preview**: View JSON configurations in real-time

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python azure_search_manager.py
   ```

3. **Access the web interface:**
   Open your browser and go to `http://localhost:8000`

## Usage

### Managing Search Index

1. **Add Fields**: Click "Add Field" to add new fields to your search index
2. **Configure Properties**: Set field properties like searchable, filterable, sortable, etc.
3. **Remove Fields**: Click the trash icon to remove unwanted fields
4. **Download**: Download the complete index configuration as JSON

### Managing Skillset

1. **Add Skills**: Click "Add Skill" to add new processing skills
2. **Configure Skills**: Set skill name, description, context, and type
3. **Remove Skills**: Click the trash icon to remove unwanted skills
4. **Download**: Download the complete skillset configuration as JSON

### File Operations

- **Upload**: Replace existing configurations by uploading new JSON files
- **Download**: Export current configurations as JSON files
- **Preview**: View formatted JSON in the web interface

## API Endpoints

### Index Management
- `GET /api/index` - Get current index configuration
- `POST /api/index` - Update index configuration
- `POST /api/index/fields` - Add new field
- `DELETE /api/index/fields/{field_name}` - Remove field

### Skillset Management
- `GET /api/skillset` - Get current skillset configuration
- `POST /api/skillset` - Update skillset configuration
- `POST /api/skillset/skills` - Add new skill
- `DELETE /api/skillset/skills/{skill_name}` - Remove skill

### File Operations
- `POST /api/upload` - Upload configuration file
- `GET /api/download/{config_type}` - Download configuration file

## Configuration Files

The application stores configurations in the `azure_configs/` directory:
- `search_index.json` - Search index configuration
- `search_skillset.json` - Skillset configuration

## Field Types

Supported Azure Cognitive Search field types:
- `Edm.String` - Text fields
- `Edm.Int32` - 32-bit integers
- `Edm.Int64` - 64-bit integers
- `Edm.Double` - Double precision numbers
- `Edm.Boolean` - Boolean values
- `Edm.DateTimeOffset` - Date/time values
- `Collection(Edm.String)` - Collections of strings

## Skill Types

Supported Azure Cognitive Search skill types:
- `Microsoft.Skills.Text.EntityRecognitionSkill` - Entity recognition
- `Microsoft.Skills.Text.SplitSkill` - Text splitting
- `Microsoft.Skills.Text.LanguageDetectionSkill` - Language detection
- `Microsoft.Skills.Text.KeyPhraseExtractionSkill` - Key phrase extraction
- `Microsoft.Skills.Text.SentimentSkill` - Sentiment analysis

## Development

### Running in Development Mode

```bash
uvicorn azure_search_manager:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

```
.
├── azure_search_manager.py    # Main FastAPI application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── templates/                # HTML templates
│   ├── dashboard.html        # Main dashboard
│   └── error.html           # Error page
└── azure_configs/           # Configuration storage
    ├── search_index.json     # Index configuration
    └── search_skillset.json # Skillset configuration
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `azure_search_manager.py`
2. **Permission errors**: Ensure write permissions for the `azure_configs/` directory
3. **JSON validation errors**: Check that uploaded files are valid JSON

### Logs

The application logs errors to the console. Check the terminal output for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
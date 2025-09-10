from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Azure Cognitive Search Manager", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# =============================================================================
# CONFIGURATION SETTINGS - Load from environment variables
# =============================================================================

from env_config import config

# Use environment configuration
CONFIG_DIR = config.CONFIG_DIR
INDEX_FILE_PATH = config.INDEX_FILE_PATH
SKILLSET_FILE_PATH = config.SKILLSET_FILE_PATH
HOST = config.HOST
PORT = config.PORT
AUTO_CREATE_SAMPLE_FILES = config.AUTO_CREATE_SAMPLE_FILES
DEBUG = config.DEBUG
ENVIRONMENT = config.ENVIRONMENT

# Create necessary directories
config.create_directories()

# Print configuration info
config.print_config()

# Pydantic models for validation
class IndexField(BaseModel):
    name: str
    type: str
    searchable: bool = True
    filterable: bool = False
    sortable: bool = False
    facetable: bool = False
    key: bool = False

class IndexConfig(BaseModel):
    name: str
    fields: List[IndexField]
    scoringProfiles: List[Dict] = []
    suggesters: List[Dict] = []
    analyzers: List[Dict] = []
    tokenizers: List[Dict] = []
    tokenFilters: List[Dict] = []
    charFilters: List[Dict] = []

class SkillSetSkill(BaseModel):
    name: str
    description: str
    context: str
    inputs: List[Dict]
    outputs: List[Dict]
    type: str = "Microsoft.Skills.Text.EntityRecognitionSkill"

class SkillSetConfig(BaseModel):
    name: str
    description: str
    skills: List[SkillSetSkill]
    cognitiveServices: Optional[Dict] = None

class SearchConfigManager:
    def __init__(self, index_file_path: str, skillset_file_path: str):
        self.index_file = index_file_path
        self.skillset_file = skillset_file_path
    
    def load_index_config(self) -> Dict:
        """Load index configuration from JSON file"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_index_config()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading index config: {str(e)}")
    
    def save_index_config(self, config: Dict) -> bool:
        """Save index configuration to JSON file"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving index config: {str(e)}")
    
    def load_skillset_config(self) -> Dict:
        """Load skillset configuration from JSON file"""
        try:
            if os.path.exists(self.skillset_file):
                with open(self.skillset_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_skillset_config()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading skillset config: {str(e)}")
    
    def save_skillset_config(self, config: Dict) -> bool:
        """Save skillset configuration to JSON file"""
        try:
            with open(self.skillset_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving skillset config: {str(e)}")
    
    def _get_default_index_config(self) -> Dict:
        """Get default index configuration"""
        return {
            "name": "default-index",
            "fields": [
                {
                    "name": "id",
                    "type": "Edm.String",
                    "key": True,
                    "searchable": False,
                    "filterable": False,
                    "sortable": False,
                    "facetable": False
                },
                {
                    "name": "content",
                    "type": "Edm.String",
                    "searchable": True,
                    "filterable": False,
                    "sortable": False,
                    "facetable": False
                }
            ],
            "scoringProfiles": [],
            "suggesters": [],
            "analyzers": [],
            "tokenizers": [],
            "tokenFilters": [],
            "charFilters": []
        }
    
    def _get_default_skillset_config(self) -> Dict:
        """Get default skillset configuration"""
        return {
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
            "cognitiveServices": None
        }
    
    def create_sample_files(self) -> bool:
        """Create sample JSON configuration files if they don't exist"""
        try:
            # Create sample index file
            if not os.path.exists(self.index_file):
                sample_index = self._get_default_index_config()
                with open(self.index_file, 'w', encoding='utf-8') as f:
                    json.dump(sample_index, f, indent=2, ensure_ascii=False)
                print(f"✅ Created sample index file: {self.index_file}")
            
            # Create sample skillset file
            if not os.path.exists(self.skillset_file):
                sample_skillset = self._get_default_skillset_config()
                with open(self.skillset_file, 'w', encoding='utf-8') as f:
                    json.dump(sample_skillset, f, indent=2, ensure_ascii=False)
                print(f"✅ Created sample skillset file: {self.skillset_file}")
            
            return True
        except Exception as e:
            print(f"❌ Error creating sample files: {e}")
            return False

# Initialize config manager
config_manager = SearchConfigManager(INDEX_FILE_PATH, SKILLSET_FILE_PATH)

# Create sample JSON files if they don't exist
if AUTO_CREATE_SAMPLE_FILES:
    config_manager.create_sample_files()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page - serve static HTML"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

@app.get("/api/index")
async def get_index_config():
    """Get current index configuration"""
    return config_manager.load_index_config()

@app.post("/api/index")
async def update_index_config(config: Dict[str, Any]):
    """Update index configuration"""
    try:
        # Validate the configuration
        index_config = IndexConfig(**config)
        config_manager.save_index_config(config)
        return {"message": "Index configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/skillset")
async def get_skillset_config():
    """Get current skillset configuration"""
    return config_manager.load_skillset_config()

@app.post("/api/skillset")
async def update_skillset_config(config: Dict[str, Any]):
    """Update skillset configuration"""
    try:
        # Validate the configuration
        skillset_config = SkillSetConfig(**config)
        config_manager.save_skillset_config(config)
        return {"message": "Skillset configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/index/fields")
async def add_index_field(
    field_name: str = Form(...),
    field_type: str = Form(...),
    searchable: bool = Form(True),
    filterable: bool = Form(False),
    sortable: bool = Form(False),
    facetable: bool = Form(False),
    is_key: bool = Form(False)
):
    """Add a new field to the index configuration"""
    try:
        config = config_manager.load_index_config()
        
        new_field = {
            "name": field_name,
            "type": field_type,
            "searchable": searchable,
            "filterable": filterable,
            "sortable": sortable,
            "facetable": facetable,
            "key": is_key
        }
        
        config["fields"].append(new_field)
        config_manager.save_index_config(config)
        
        return {"message": f"Field '{field_name}' added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/index/fields/{field_name}")
async def remove_index_field(field_name: str):
    """Remove a field from the index configuration"""
    try:
        config = config_manager.load_index_config()
        config["fields"] = [f for f in config["fields"] if f["name"] != field_name]
        config_manager.save_index_config(config)
        
        return {"message": f"Field '{field_name}' removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/skillset/skills")
async def add_skillset_skill(
    skill_name: str = Form(...),
    skill_description: str = Form(...),
    skill_context: str = Form(...),
    skill_type: str = Form("Microsoft.Skills.Text.EntityRecognitionSkill")
):
    """Add a new skill to the skillset configuration"""
    try:
        config = config_manager.load_skillset_config()
        
        new_skill = {
            "name": skill_name,
            "description": skill_description,
            "context": skill_context,
            "inputs": [],
            "outputs": [],
            "type": skill_type
        }
        
        config["skills"].append(new_skill)
        config_manager.save_skillset_config(config)
        
        return {"message": f"Skill '{skill_name}' added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/skillset/skills/{skill_name}")
async def remove_skillset_skill(skill_name: str):
    """Remove a skill from the skillset configuration"""
    try:
        config = config_manager.load_skillset_config()
        config["skills"] = [s for s in config["skills"] if s["name"] != skill_name]
        config_manager.save_skillset_config(config)
        
        return {"message": f"Skill '{skill_name}' removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/upload")
async def upload_config_file(file: UploadFile = File(...)):
    """Upload and replace configuration files"""
    try:
        content = await file.read()
        config_data = json.loads(content.decode('utf-8'))
        
        # Check file extension and determine type
        if file.filename and file.filename.endswith('.json'):
            if 'index' in file.filename.lower() or 'search' in file.filename.lower():
                config_manager.save_index_config(config_data)
                return {
                    "message": "Index configuration uploaded successfully",
                    "file_path": INDEX_FILE_PATH,
                    "file_name": file.filename
                }
            elif 'skill' in file.filename.lower():
                config_manager.save_skillset_config(config_data)
                return {
                    "message": "Skillset configuration uploaded successfully",
                    "file_path": SKILLSET_FILE_PATH,
                    "file_name": file.filename
                }
            else:
                # Try to determine type from content structure
                if 'fields' in config_data:
                    config_manager.save_index_config(config_data)
                    return {
                        "message": "Index configuration uploaded successfully (detected from content)",
                        "file_path": INDEX_FILE_PATH,
                        "file_name": file.filename
                    }
                elif 'skills' in config_data:
                    config_manager.save_skillset_config(config_data)
                    return {
                        "message": "Skillset configuration uploaded successfully (detected from content)",
                        "file_path": SKILLSET_FILE_PATH,
                        "file_name": file.filename
                    }
                else:
                    raise HTTPException(status_code=400, detail="Cannot determine configuration type. File must contain 'fields' (index) or 'skills' (skillset)")
        else:
            raise HTTPException(status_code=400, detail="File must have .json extension")
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{config_type}")
async def download_config(config_type: str):
    """Download configuration files"""
    try:
        if config_type == "index":
            config = config_manager.load_index_config()
            filename = "search_index.json"
        elif config_type == "skillset":
            config = config_manager.load_skillset_config()
            filename = "search_skillset.json"
        else:
            raise HTTPException(status_code=400, detail="Invalid config type")
        
        return JSONResponse(
            content=config,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config/paths")
async def get_config_paths():
    """Get current configuration file paths"""
    return {
        "config_directory": CONFIG_DIR,
        "index_file_path": INDEX_FILE_PATH,
        "skillset_file_path": SKILLSET_FILE_PATH,
        "index_file_exists": os.path.exists(INDEX_FILE_PATH),
        "skillset_file_exists": os.path.exists(SKILLSET_FILE_PATH)
    }

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
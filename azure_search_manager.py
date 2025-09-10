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

# Configuration directory
CONFIG_DIR = "azure_configs"
os.makedirs(CONFIG_DIR, exist_ok=True)

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
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.index_file = os.path.join(config_dir, "search_index.json")
        self.skillset_file = os.path.join(config_dir, "search_skillset.json")
    
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

# Initialize config manager
config_manager = SearchConfigManager(CONFIG_DIR)

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
        
        if file.filename == "search_index.json":
            config_manager.save_index_config(config_data)
            return {"message": "Index configuration uploaded successfully"}
        elif file.filename == "search_skillset.json":
            config_manager.save_skillset_config(config_data)
            return {"message": "Skillset configuration uploaded successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid file name. Use 'search_index.json' or 'search_skillset.json'")
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
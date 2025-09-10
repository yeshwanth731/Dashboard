# Static Files Integration Guide

## 📁 Project Structure

Your Azure Cognitive Search Manager now has a complete static file structure:

```
/workspace/
├── azure_search_manager.py    # Main FastAPI application
├── static/                    # Static files directory
│   ├── index.html             # Main HTML page
│   ├── css/
│   │   └── style.css          # Custom CSS styles
│   ├── js/
│   │   └── main.js            # JavaScript functionality
│   └── images/                # Images directory (empty)
├── templates/                 # Jinja2 templates (legacy)
├── azure_configs/             # Configuration storage
└── requirements.txt           # Python dependencies
```

## 🔧 How Static Files Connect with FastAPI

### 1. **FastAPI Static File Mounting**
```python
# In azure_search_manager.py
app.mount("/static", StaticFiles(directory="static"), name="static")
```
This tells FastAPI to serve files from the `static/` directory at the `/static/` URL path.

### 2. **HTML References Static Files**
```html
<!-- In static/index.html -->
<link href="/static/css/style.css" rel="stylesheet">
<script src="/static/js/main.js"></script>
```
The `/static/` prefix maps to the `static/` directory on disk.

### 3. **JavaScript Makes API Calls**
```javascript
// In static/js/main.js
fetch('/api/index')  // Calls FastAPI endpoint
fetch('/api/skillset')  // Calls FastAPI endpoint
```

## 🚀 How to Run

### Option 1: Using the startup script
```bash
python3 start_server.py
```

### Option 2: Direct FastAPI
```bash
# Install dependencies first
pip3 install -r requirements.txt --break-system-packages

# Run the server
python3 azure_search_manager.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn azure_search_manager:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Access Points

- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Static Files**: 
  - CSS: http://localhost:8000/static/css/style.css
  - JS: http://localhost:8000/static/js/main.js
  - HTML: http://localhost:8000/static/index.html

## 📋 Features

### HTML (`static/index.html`)
- ✅ Responsive Bootstrap-based UI
- ✅ Modal dialogs for adding fields/skills
- ✅ Real-time JSON preview
- ✅ File upload/download functionality
- ✅ Help documentation modal

### CSS (`static/css/style.css`)
- ✅ Custom styling for Azure theme
- ✅ Responsive design for mobile/tablet
- ✅ Smooth animations and transitions
- ✅ Dark theme JSON viewer
- ✅ Professional color scheme

### JavaScript (`static/js/main.js`)
- ✅ ES6 class-based architecture
- ✅ Async/await API calls
- ✅ Dynamic DOM manipulation
- ✅ Form validation and submission
- ✅ Error handling and user feedback
- ✅ Real-time configuration updates

## 🔄 Data Flow

1. **User opens browser** → `http://localhost:8000`
2. **FastAPI serves** → `static/index.html`
3. **HTML loads** → CSS and JS files from `/static/`
4. **JavaScript executes** → Makes API calls to `/api/*`
5. **FastAPI responds** → JSON data for configuration
6. **JavaScript updates** → DOM with new data
7. **User interactions** → Trigger more API calls

## 🛠️ Customization

### Adding New Static Files
1. Place files in appropriate subdirectory (`css/`, `js/`, `images/`)
2. Reference them in HTML with `/static/path/to/file`
3. FastAPI automatically serves them

### Modifying Styles
- Edit `static/css/style.css`
- Changes are immediately visible (no restart needed)
- Use browser dev tools for live editing

### Adding JavaScript Features
- Edit `static/js/main.js`
- Add new methods to `AzureSearchManager` class
- Use `fetch()` for API calls
- Update HTML to call new functions

## 🐛 Troubleshooting

### Static Files Not Loading
- Check file paths start with `/static/`
- Verify files exist in `static/` directory
- Check browser console for 404 errors

### JavaScript Errors
- Open browser dev tools (F12)
- Check console for error messages
- Verify API endpoints are working

### CSS Not Applying
- Check CSS file is loading in Network tab
- Verify selectors match HTML elements
- Use browser dev tools to inspect styles

## 📱 Mobile Responsiveness

The static files include responsive design:
- ✅ Mobile-first CSS approach
- ✅ Bootstrap grid system
- ✅ Touch-friendly buttons
- ✅ Collapsible navigation
- ✅ Optimized for tablets and phones

## 🔒 Security Notes

- Static files are served directly by FastAPI
- No authentication required for static files
- API endpoints have validation and error handling
- File uploads are validated for JSON format

## 🎨 Theme Customization

To change the color scheme, modify CSS variables in `style.css`:
```css
:root {
    --primary-color: #0078d4;    /* Azure blue */
    --secondary-color: #6c757d;  /* Gray */
    --success-color: #28a745;    /* Green */
    --danger-color: #dc3545;     /* Red */
}
```

This creates a complete, professional web application for managing Azure Cognitive Search configurations with a clean separation between static assets and dynamic API functionality.
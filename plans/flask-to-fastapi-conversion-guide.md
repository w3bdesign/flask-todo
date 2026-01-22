# Flask to FastAPI Conversion Guide

A comprehensive learning guide for converting the Flask Todo app to FastAPI.

## Table of Contents

1. [Overview](#overview)
2. [Key Differences Between Flask and FastAPI](#key-differences)
3. [Project Structure Comparison](#project-structure)
4. [Step-by-Step Conversion Process](#conversion-process)
5. [Code Comparisons](#code-comparisons)
6. [Benefits of Migration](#benefits)
7. [Common Patterns and Best Practices](#patterns)
8. [Testing Strategy](#testing)

## Overview

This guide demonstrates how to convert a Flask web application to FastAPI while maintaining the same functionality. The original Flask app is a todo list application with both web interface (HTML templates) and API endpoints.

### Current Flask App Features
- **Web Interface**: Jinja2 templates with Tailwind CSS
- **API Endpoints**: JSON responses for CRUD operations
- **Form Handling**: POST forms for creating/editing todos
- **Static Files**: CSS and assets
- **In-Memory Storage**: Simple list-based data storage

## Key Differences Between Flask and FastAPI

### Framework Philosophy

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| **Type System** | Optional type hints | Built-in type validation with Pydantic |
| **API Documentation** | Manual (Swagger/OpenAPI optional) | Automatic OpenAPI/Swagger generation |
| **Async Support** | Via extensions | Native async/await support |
| **Request Validation** | Manual validation | Automatic with type hints |
| **Performance** | WSGI-based | ASGI-based (faster) |
| **Learning Curve** | Minimal, flexible | Moderate, but more structured |

### Syntax Differences

**Flask Route Definition:**
```python
@app.route("/items/<int:item_id>", methods=["GET", "POST"])
def handle_item(item_id):
    if request.method == "POST":
        # Handle POST
        pass
    # Handle GET
```

**FastAPI Equivalent:**
```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Handle GET only
    pass

@app.post("/items/{item_id}")
async def update_item(item_id: int, item_data: ItemModel):
    # Handle POST with automatic validation
    pass
```

## Project Structure Comparison

### Flask Structure (Current)
```
flask-todo/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── package.json          # Frontend build
├── templates/            # Jinja2 templates
│   ├── index.html
│   ├── create.html
│   └── edit.html
├── static/               # Static files
│   ├── css/main.css
│   └── src/input.css
└── README.md
```

### FastAPI Structure (Proposed)
```
fastapi-todo/
├── main.py               # FastAPI application
├── models.py             # Pydantic models
├── crud.py               # CRUD operations
├── requirements.txt      # FastAPI dependencies
├── package.json          # Frontend build
├── templates/            # Jinja2 templates (adapted)
│   ├── index.html
│   ├── create.html
│   └── edit.html
├── static/               # Static files
│   ├── css/main.css
│   └── src/input.css
└── README.md            # Updated setup guide
```

## Step-by-Step Conversion Process

### Step 1: Dependencies Update

**Flask requirements.txt:**
```txt
Flask==3.1.2
Jinja2==3.1.6
requests==2.32.5
```

**FastAPI requirements.txt:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.6
python-multipart==0.0.6
aiofiles==23.2.1
requests==2.32.5
```

### Step 2: Application Setup

**Flask Setup ([`app.py`](../app.py)):**
```python
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Routes defined with @app.route()
```

**FastAPI Setup (main.py):**
```python
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")
```

### Step 3: Data Models

**Flask (No formal models):**
```python
# Data handled as dictionaries
todo = {"id": 1, "title": "Sample", "description": "Description"}
todos = []  # Global list
```

**FastAPI (Pydantic Models):**
```python
# models.py
from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: str

class Todo(BaseModel):
    id: int
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
```

### Step 4: Route Conversion

#### API Routes

**Flask API Route:**
```python
@app.route("/todos")
def get_all_todos():
    return jsonify({"todos": todos})

@app.route("/todos/<int:id>")
def get_todo_by_id(id):
    todo = find_todo_by_id(id)
    if todo:
        return jsonify({"todo": todo})
    else:
        return jsonify({"error": "Todo not found."}), 404
```

**FastAPI API Route:**
```python
from typing import List

@app.get("/todos", response_model=List[Todo])
async def get_all_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

#### Web Interface Routes

**Flask Template Route:**
```python
@app.route("/")
def index():
    response = requests.get("http://localhost:5000/todos")
    todos = response.json()["todos"]
    return render_template("index.html", todos=todos)
```

**FastAPI Template Route:**
```python
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "todos": todos}
    )
```

#### Form Handling

**Flask Form Processing:**
```python
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = {"id": generate_id(), "title": title, "description": description}
        create_todo(todo)
        return redirect(url_for("index"))
    return render_template("create.html")
```

**FastAPI Form Processing:**
```python
@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
async def create_todo_form(
    request: Request,
    title: str = Form(...),
    description: str = Form(...)
):
    todo = Todo(id=generate_id(), title=title, description=description)
    create_todo(todo)
    return RedirectResponse(url="/", status_code=303)
```

### Step 5: Template Updates

**Flask Template ([`templates/index.html`](../templates/index.html)):**
```html
<link href="{{url_for('static',filename='css/main.css')}}" rel="stylesheet" />
<a href="/edit/{{ todo.id }}">Edit</a>
```

**FastAPI Template (minimal changes):**
```html
<link href="{{ url_for('static', path='/css/main.css') }}" rel="stylesheet" />
<a href="/edit/{{ todo.id }}">Edit</a>
```

## Code Comparisons

### Complete Route Comparison

#### Flask Version (Original)
```python
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        update_todo_by_id(id, {"title": title, "description": description})
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)
```

#### FastAPI Version (Converted)
```python
@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int):
    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, "todo": todo}
    )

@app.post("/edit/{todo_id}")
async def edit_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form(...)
):
    update_data = {"title": title, "description": description}
    updated_todo = update_todo_by_id(todo_id, update_data)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return RedirectResponse(url="/", status_code=303)
```

### Error Handling Comparison

**Flask Error Handling:**
```python
try:
    todo = get_todo_by_id(id)
    return jsonify({"todo": todo})
except Exception:
    return jsonify({"error": "Todo not found"}), 404
```

**FastAPI Error Handling:**
```python
from fastapi import HTTPException

todo = get_todo_by_id(id)
if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
return todo
```

## Benefits of Migration

### 1. Automatic API Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

### 2. Type Safety and Validation
```python
# FastAPI automatically validates this
@app.post("/todos/")
async def create_todo(todo: TodoCreate):
    # todo.title is guaranteed to be a string
    # todo.description is guaranteed to be a string
    pass
```

### 3. Performance Improvements
- **ASGI vs WSGI**: FastAPI uses ASGI, which is faster than Flask's WSGI
- **Async Support**: Native support for async operations
- **Efficient Serialization**: Pydantic models are faster than manual JSON handling

### 4. Better Developer Experience
- **IDE Support**: Better autocomplete and type checking
- **Error Messages**: More descriptive validation errors
- **Standards**: Built on modern Python standards (type hints, async/await)

## Common Patterns and Best Practices

### 1. Dependency Injection
```python
# Instead of global variables, use dependency injection
def get_todo_service():
    return TodoService()

@app.get("/todos/")
async def get_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_all()
```

### 2. Response Models
```python
# Define what the API returns
@app.get("/todos/", response_model=List[Todo])
async def get_todos():
    # FastAPI ensures response matches Todo model
    return todos
```

### 3. Request Validation
```python
# Automatic validation of request body
@app.post("/todos/")
async def create_todo(todo: TodoCreate):
    # todo is already validated
    pass
```

### 4. Exception Handling
```python
# Custom exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )
```

## Testing Strategy

### Flask Testing
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_todos(client):
    rv = client.get('/todos')
    assert rv.status_code == 200
```

### FastAPI Testing
```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Migration Checklist

### Pre-Migration
- [ ] Analyze current Flask routes and functionality
- [ ] Identify data models needed
- [ ] Plan project structure
- [ ] Set up development environment

### Core Migration
- [ ] Create FastAPI application structure
- [ ] Define Pydantic models
- [ ] Convert API routes
- [ ] Convert web interface routes
- [ ] Update templates for FastAPI
- [ ] Handle static files
- [ ] Update form processing

### Post-Migration
- [ ] Test all endpoints
- [ ] Verify template rendering
- [ ] Check static file serving
- [ ] Test form submissions
- [ ] Validate API documentation
- [ ] Performance testing

### Optional Enhancements
- [ ] Add async database operations
- [ ] Implement proper authentication
- [ ] Add request/response logging
- [ ] Set up background tasks
- [ ] Add caching layer

## Conclusion

Converting from Flask to FastAPI involves:

1. **Structural Changes**: Separating concerns into models, routes, and services
2. **Syntax Updates**: Using FastAPI decorators and dependencies
3. **Type Safety**: Adding Pydantic models for validation
4. **Template Adjustments**: Minor changes to Jinja2 templates
5. **Enhanced Features**: Gaining automatic documentation and validation

The migration provides significant benefits in terms of performance, developer experience, and API standards compliance while maintaining the same user-facing functionality.

The key is to approach it systematically, converting one route at a time and testing thoroughly. The modular approach makes it easy to validate each component as you migrate.

This learning exercise demonstrates modern Python web development practices and prepares you for building scalable, well-documented APIs with FastAPI.
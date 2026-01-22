"""
FastAPI Todo Application - Main Entry Point

This is the FastAPI equivalent of app.py (Flask version).

To run this application:
    uvicorn main:app --reload --port 8000

Then visit:
    http://localhost:8000/       - Web interface
    http://localhost:8000/docs   - Swagger API documentation
    http://localhost:8000/redoc  - ReDoc API documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import our Pydantic models
from models import Todo, TodoCreate, TodoUpdate

# =============================================================================
# Application Setup
# =============================================================================

app = FastAPI(
    title="Todo App",
    description="A simple todo application - converted from Flask to FastAPI",
    version="1.0.0",
)

# Mount static files (CSS, JS, images)
# This makes files in ./static available at /static URL
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates (same template engine as Flask)
templates = Jinja2Templates(directory="templates")

# =============================================================================
# In-Memory Data Storage (same as Flask version)
# =============================================================================

todos: list[dict] = []


def generate_id() -> int:
    """Generate a unique ID for a new todo."""
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1


def find_todo_by_id(todo_id: int) -> dict | None:
    """Find a todo by its ID. Returns None if not found."""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


# =============================================================================
# Phase 2: API Routes (JSON endpoints)
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the app is running."""
    return {"status": "healthy", "message": "FastAPI Todo App is running!"}


@app.get("/todos")
async def get_all_todos():
    """
    Get all todos.
    
    Flask equivalent:
        @app.route("/todos")
        def get_all_todos():
            return jsonify({"todos": todos})
    
    FastAPI differences:
        - Uses @app.get() instead of @app.route()
        - Returns dict directly (auto-converted to JSON)
        - async function (optional but recommended)
    """
    return {"todos": todos}


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    """
    Get a single todo by ID.
    
    Flask equivalent:
        @app.route("/todos/<int:id>")
        def get_todo_by_id(id):
            todo = find_todo_by_id(id)
            if todo:
                return jsonify({"todo": todo})
            else:
                return jsonify({"error": "Todo not found."}), 404
    
    FastAPI differences:
        - Path parameter: {todo_id} instead of <int:id>
        - Type hint: todo_id: int (automatic validation)
        - HTTPException instead of returning tuple with status code
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"todo": todo}


# =============================================================================
# Phase 3: Web Interface Routes (HTML pages) - Coming next
# =============================================================================

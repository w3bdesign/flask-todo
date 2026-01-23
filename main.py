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

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# Import our Pydantic models
from models import Todo

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
# In-Memory Data Storage (using Pydantic models!)
# =============================================================================

# Store todos as Pydantic model instances for type safety
todos: list[Todo] = []


def generate_id() -> int:
    """Generate a unique ID for a new todo."""
    if not todos:
        return 1
    return max(todo.id for todo in todos) + 1


def find_todo_by_id(todo_id: int) -> Todo | None:
    """Find a todo by its ID. Returns None if not found."""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None


# =============================================================================
# Phase 2: API Routes (JSON endpoints)
# =============================================================================


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the app is running."""
    return {"status": "healthy", "message": "FastAPI Todo App is running!"}


@app.get("/todos", response_model=list[Todo])
async def get_all_todos():
    """
    Get all todos.

    Flask equivalent:
        @app.route("/todos")
        def get_all_todos():
            return jsonify({"todos": todos})

    FastAPI with Pydantic:
        - response_model=list[Todo] ensures proper JSON serialization
        - Automatic documentation of response schema
        - Type validation on output
    """
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """
    Get a single todo by ID.

    Flask equivalent:
        @app.route("/todos/<int:id>")
        def get_todo_by_id(id):
            ...

    FastAPI with Pydantic:
        - response_model=Todo ensures proper serialization
        - Path parameter validation with type hint
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# =============================================================================
# Phase 3: Web Interface Routes (HTML pages)
# =============================================================================


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Homepage - displays all todos.

    We convert Pydantic models to dicts for template rendering.
    """
    # Convert Pydantic models to dicts for Jinja2 template
    todos_dict = [todo.model_dump() for todo in todos]
    return templates.TemplateResponse(request, "index.html", {"todos": todos_dict})


@app.post("/", response_class=HTMLResponse)
async def create_todo(
    request: Request, title: str = Form(...), description: str = Form("")
):
    """
    Handle inline create form submission from homepage.

    Creates a new Todo using Pydantic model for validation.
    """
    # Create Pydantic model instance (validates the data!)
    todo = Todo(id=generate_id(), title=title, description=description)
    todos.append(todo)
    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int):
    """Show the edit form for a specific todo."""
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Convert to dict for template
    return templates.TemplateResponse(request, "edit.html", {"todo": todo.model_dump()})


@app.post("/edit/{todo_id}")
async def edit_todo(todo_id: int, title: str = Form(...), description: str = Form("")):
    """
    Handle edit form submission.

    Updates the todo using Pydantic model.
    """
    # Find existing todo
    old_todo = find_todo_by_id(todo_id)
    if not old_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Create updated todo with Pydantic validation
    # Keep the completed status from the original todo
    updated_todo = Todo(
        id=todo_id,
        title=title,
        description=description,
        completed=old_todo.completed,  # Preserve completed status
    )

    # Replace old with new
    index = todos.index(old_todo)
    todos[index] = updated_todo

    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo and redirect to homepage."""
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todos.remove(todo)
    return RedirectResponse(url="/", status_code=303)


# =============================================================================
# Phase 7: Toggle Completed Status (New Feature!)
# =============================================================================


@app.get("/toggle/{todo_id}")
async def toggle_completed(todo_id: int):
    """
    Toggle the completed status of a todo.

    This is a NEW feature not in the original Flask app!
    It demonstrates how easy it is to add features in FastAPI.

    How it works:
    1. Find the todo by ID
    2. Create a new todo with completed = not completed
    3. Replace the old todo with the new one
    4. Redirect back to homepage
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Create updated todo with toggled completed status
    updated_todo = Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=not todo.completed,  # Toggle: True becomes False, False becomes True
    )

    # Replace old with new
    index = todos.index(todo)
    todos[index] = updated_todo

    return RedirectResponse(url="/", status_code=303)

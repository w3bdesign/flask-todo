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
# Phase 3: Web Interface Routes (HTML pages)
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Homepage - displays all todos.
    
    Flask equivalent:
        @app.route("/")
        def index():
            response = requests.get("http://localhost:5000/todos")
            todos = response.json()["todos"]
            return render_template("index.html", todos=todos)
    
    FastAPI differences:
        - response_class=HTMLResponse tells FastAPI this returns HTML
        - request: Request is required for templates
        - templates.TemplateResponse instead of render_template
        - We access todos directly (no need to call our own API)
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": todos}
    )


@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    """
    Show the create todo form.
    
    Flask equivalent:
        @app.route("/create", methods=["GET", "POST"])
        def create():
            if request.method == "POST":
                ...
            return render_template("create.html")
    
    FastAPI differences:
        - Separate routes for GET and POST (cleaner!)
        - This handles only GET (showing the form)
    """
    return templates.TemplateResponse(
        "create.html",
        {"request": request}
    )


@app.post("/create")
async def create_todo(
    title: str = Form(...),
    description: str = Form("")
):
    """
    Handle create form submission.
    
    Flask equivalent:
        @app.route("/create", methods=["POST"])
        def create():
            title = request.form["title"]
            description = request.form["description"]
            todo = {"id": generate_id(), "title": title, "description": description}
            create_todo(todo)
            return redirect(url_for("index"))
    
    FastAPI differences:
        - Form(...) extracts form data (requires python-multipart)
        - Type hints provide validation
        - RedirectResponse instead of redirect()
        - status_code=303 is important for POST->GET redirect
    """
    todo = {
        "id": generate_id(),
        "title": title,
        "description": description
    }
    todos.append(todo)
    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int):
    """
    Show the edit form for a specific todo.
    
    Flask equivalent:
        @app.route("/edit/<int:id>", methods=["GET"])
        def edit(id):
            todo = get_todo_by_id(id)
            return render_template("edit.html", todo=todo)
    """
    todo = find_todo_by_id(todo_id)
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
    description: str = Form("")
):
    """
    Handle edit form submission.
    
    Flask equivalent:
        @app.route("/edit/<int:id>", methods=["POST"])
        def edit(id):
            title = request.form["title"]
            description = request.form["description"]
            update_todo_by_id(id, {"title": title, "description": description})
            return redirect(url_for("index"))
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo["title"] = title
    todo["description"] = description
    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    """
    Delete a todo and redirect to homepage.
    
    Flask equivalent:
        @app.route("/delete/<int:id>")
        def delete(id):
            delete_todo_by_id(id)
            return redirect(url_for("index"))
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todos.remove(todo)
    return RedirectResponse(url="/", status_code=303)

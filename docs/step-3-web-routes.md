# Step 3: Web Interface Routes Conversion

This document explains how to convert Flask's HTML-serving routes to FastAPI.

## Overview

Web routes serve HTML pages with forms for user interaction. These are different from API routes because they:
- Return HTML instead of JSON
- Handle form submissions
- Use redirects after POST requests

## Routes Converted

| Route | Method | Flask | FastAPI | Purpose |
|-------|--------|-------|---------|---------|
| `/` | GET | `@app.route("/")` | `@app.get("/")` | Homepage |
| `/create` | GET | `@app.route("/create")` | `@app.get("/create")` | Show form |
| `/create` | POST | `@app.route("/create", methods=["POST"])` | `@app.post("/create")` | Handle form |
| `/edit/{id}` | GET | `@app.route("/edit/<int:id>")` | `@app.get("/edit/{todo_id}")` | Show edit form |
| `/edit/{id}` | POST | Same with methods=["POST"] | `@app.post("/edit/{todo_id}")` | Handle edit |
| `/delete/{id}` | GET | `@app.route("/delete/<int:id>")` | `@app.get("/delete/{todo_id}")` | Delete & redirect |

## Code Comparison

### Homepage Route

**Flask:**
```python
@app.route("/")
def index():
    response = requests.get("http://localhost:5000/todos")
    todos = response.json()["todos"]
    return render_template("index.html", todos=todos)
```

**FastAPI:**
```python
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    todos_dict = [todo.model_dump() for todo in todos]
    return templates.TemplateResponse(
        request,
        "index.html",
        {"todos": todos_dict}
    )
```

**Key Differences:**
1. `response_class=HTMLResponse` declares we're returning HTML
2. `request: Request` parameter is required for templates
3. `templates.TemplateResponse()` instead of `render_template()`
4. Request must be passed as first argument (new Starlette syntax)

### Create Form - GET (Show Form)

**Flask:**
```python
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # handle POST
    return render_template("create.html")
```

**FastAPI:**
```python
@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    return templates.TemplateResponse(request, "create.html")
```

**Key Difference:** FastAPI separates GET and POST into different functions!

### Create Form - POST (Handle Submission)

**Flask:**
```python
@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    description = request.form["description"]
    todo = {"id": generate_id(), "title": title, "description": description}
    create_todo(todo)
    return redirect(url_for("index"))
```

**FastAPI:**
```python
@app.post("/create")
async def create_todo(
    title: str = Form(...),
    description: str = Form("")
):
    todo = Todo(id=generate_id(), title=title, description=description)
    todos.append(todo)
    return RedirectResponse(url="/", status_code=303)
```

**Key Differences:**

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| Form data | `request.form["title"]` | `title: str = Form(...)` |
| Required field | Raises KeyError if missing | `Form(...)` - automatically validates |
| Optional field | `request.form.get("desc", "")` | `Form("")` - default value |
| Redirect | `redirect(url_for("index"))` | `RedirectResponse(url="/", status_code=303)` |

### Why Status Code 303?

The `status_code=303` is important! Here's why:

```python
# This is correct for form submissions
return RedirectResponse(url="/", status_code=303)

# NOT this (would cause issues)
return RedirectResponse(url="/")  # Default is 307
```

- **303 See Other**: Browser will GET the redirect URL (what we want after POST)
- **307 Temporary Redirect**: Browser will POST to the redirect URL (causes issues!)

### Edit Route

**Flask:**
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

**FastAPI (GET):**
```python
@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int):
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse(
        request,
        "edit.html",
        {"todo": todo.model_dump()}
    )
```

**FastAPI (POST):**
```python
@app.post("/edit/{todo_id}")
async def edit_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form("")
):
    old_todo = find_todo_by_id(todo_id)
    if not old_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    updated_todo = Todo(id=todo_id, title=title, description=description)
    index = todos.index(old_todo)
    todos[index] = updated_todo
    
    return RedirectResponse(url="/", status_code=303)
```

### Delete Route

**Flask:**
```python
@app.route("/delete/<int:id>")
def delete(id):
    delete_todo_by_id(id)
    return redirect(url_for("index"))
```

**FastAPI:**
```python
@app.get("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.remove(todo)
    return RedirectResponse(url="/", status_code=303)
```

## Form(...) Explained

The `Form(...)` function is how FastAPI handles form data:

```python
from fastapi import Form

# Required field (... means required)
title: str = Form(...)

# Optional field with default
description: str = Form("")

# Optional field that can be None
maybe_value: str | None = Form(None)
```

**Important:** You need `python-multipart` installed for form handling:
```bash
pip install python-multipart
```

## TemplateResponse Explained

The new Starlette syntax for templates:

```python
# Old syntax (deprecated, causes warnings)
return templates.TemplateResponse(
    "template.html",
    {"request": request, "data": data}
)

# New syntax (correct)
return templates.TemplateResponse(
    request,           # Request as first argument
    "template.html",   # Template name second
    {"data": data}     # Context dict (no need to include request)
)
```

## Verification

Test your web routes:

1. **Homepage**: Visit http://localhost:8000/
2. **Create form**: Click "Create New Todo"
3. **Submit form**: Fill in title, click Create
4. **Edit**: Click "Edit" on a todo
5. **Delete**: Click "Delete" on a todo

All should work without errors!

## Key Learning Points

1. **Separate routes for GET/POST** - FastAPI uses different decorators
2. **Form parameters** - Declared in function signature with `Form()`
3. **Status code 303** - Essential for POST redirect pattern
4. **Request parameter** - Required for template responses
5. **Pydantic integration** - Create model instances from form data

## Next Step

Proceed to **Step 4: Template Updates** to learn about the template changes needed.

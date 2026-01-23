# Step 3: Web Routes (The Pages You See)

## 🎯 What You'll Learn

In this step, you'll learn how to convert the **web pages** of your Flask app to FastAPI. These are the pages users actually see and interact with:

- 📋 **Homepage** - Shows all your todos
- ➕ **Create page** - Form to add a new todo
- ✏️ **Edit page** - Form to change a todo
- 🗑️ **Delete** - Removes a todo

---

## 🔄 The Big Picture

Here's what we're converting:

| Page | What it does | Flask URL | FastAPI URL |
|------|--------------|-----------|-------------|
| Homepage | Shows all todos | `/` | `/` (same!) |
| Create form | New todo form | `/create` | `/create` (same!) |
| Edit form | Edit a todo | `/edit/1` | `/edit/1` (same!) |
| Delete | Remove a todo | `/delete/1` | `/delete/1` (same!) |

**Great news:** The URLs stay exactly the same! Only the Python code changes.

---

## 📖 Route #1: The Homepage

This is the main page that shows all your todos.

### Flask Version:
```python
@app.route("/")
def index():
    return render_template("index.html", todos=todos)
```

### FastAPI Version:
```python
@app.get("/")
async def index(request: Request):
    todos_dict = [todo.model_dump() for todo in todos]
    return templates.TemplateResponse(
        request,
        "index.html",
        {"todos": todos_dict}
    )
```

### What Changed? 🤔

| Flask | FastAPI | Why? |
|-------|---------|------|
| `@app.route("/")` | `@app.get("/")` | FastAPI wants to know the HTTP method (GET, POST, etc.) |
| `def index()` | `async def index(request: Request)` | FastAPI needs the request object for templates |
| `render_template(...)` | `templates.TemplateResponse(...)` | Different function name, same result! |

---

## 📖 Route #2: The Create Page

In Flask, one function handles both **showing the form** and **submitting it**. In FastAPI, we split these into **two separate functions**. This makes the code cleaner!

### Flask Version (one function does both):
```python
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # Handle form submission
        title = request.form["title"]
        description = request.form["description"]
        # ... create the todo ...
        return redirect(url_for("index"))
    # Show the form
    return render_template("create.html")
```

### FastAPI Version (two separate functions):

**Function 1: Show the form (GET request)**
```python
@app.get("/create")
async def create_form(request: Request):
    return templates.TemplateResponse(request, "create.html")
```

**Function 2: Handle submission (POST request)**
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

### What's Different? 🤔

1. **Two functions instead of one** - Cleaner and easier to understand!
2. **Form data is in the function parameters** - No more `request.form["title"]`
3. **`Form(...)` means "this field is required"** - FastAPI checks it for you!
4. **`Form("")` means "optional, default to empty"**

---

## 💡 Understanding Form(...)

This is one of the coolest parts of FastAPI!

```python
async def create_todo(
    title: str = Form(...),        # Required! User must fill this in
    description: str = Form("")    # Optional, defaults to empty string
):
```

- `Form(...)` = **Required field** (the `...` is Python's way of saying "no default")
- `Form("")` = **Optional field** with a default value of `""`

If someone submits without a title, FastAPI automatically returns an error - you don't have to write that code yourself!

---

## 📖 Route #3: The Edit Page

Same pattern as create - two functions instead of one.

### Flask Version:
```python
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        # Handle the update
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)
```

### FastAPI Version:

**Show the edit form:**
```python
@app.get("/edit/{todo_id}")
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

**Handle the edit:**
```python
@app.post("/edit/{todo_id}")
async def edit_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form("")
):
    # Update logic here...
    return RedirectResponse(url="/", status_code=303)
```

### Notice the URL Pattern Change:

| Flask | FastAPI |
|-------|---------|
| `/edit/<int:id>` | `/edit/{todo_id}` |

- Flask uses `<int:id>` 
- FastAPI uses `{todo_id}` with type hint `todo_id: int`

---

## 📖 Route #4: Delete

Delete is simpler - just one function since there's no form.

### Flask Version:
```python
@app.route("/delete/<int:id>")
def delete(id):
    delete_todo_by_id(id)
    return redirect(url_for("index"))
```

### FastAPI Version:
```python
@app.get("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.remove(todo)
    return RedirectResponse(url="/", status_code=303)
```

---

## ⚠️ Important: Status Code 303

You'll notice we use `status_code=303` for redirects:

```python
return RedirectResponse(url="/", status_code=303)
```

**Why 303?** 

After you submit a form (POST), you want the browser to **go to a new page** (GET). Status code 303 tells the browser: "Go to this URL using GET, not POST."

Without 303, you might get weird behavior like the browser trying to submit the form again!

---

## 🧪 Test Your Routes

1. **Start the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Test each page:**
   - Go to http://localhost:8000 - See the todo list ✓
   - Click "Create New Todo" - See the form ✓
   - Fill in the form and submit - Back to homepage with new todo ✓
   - Click "Edit" on a todo - See edit form with current values ✓
   - Change something and save - Back to homepage with changes ✓
   - Click "Delete" - Todo is gone ✓

---

## 🎓 Quick Summary

| Concept | Flask | FastAPI |
|---------|-------|---------|
| Route decorator | `@app.route("/path")` | `@app.get("/path")` or `@app.post("/path")` |
| URL parameters | `<int:id>` | `{todo_id}` + type hint |
| Get form data | `request.form["field"]` | `field: str = Form(...)` |
| Show template | `render_template("x.html", data=data)` | `templates.TemplateResponse(request, "x.html", {"data": data})` |
| Redirect | `redirect(url_for("index"))` | `RedirectResponse(url="/", status_code=303)` |

---

## ⏭️ What's Next?

In **Step 4**, we'll update the HTML templates (don't worry, it's just one tiny change!).

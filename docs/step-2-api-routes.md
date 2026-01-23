# Step 2: API Routes Conversion

This document explains the API route conversion from Flask to FastAPI.

## Routes Converted

| Endpoint | Flask | FastAPI | Purpose |
|----------|-------|---------|---------|
| `GET /todos` | `@app.route("/todos")` | `@app.get("/todos")` | List all todos |
| `GET /todos/{id}` | `@app.route("/todos/<int:id>")` | `@app.get("/todos/{todo_id}")` | Get single todo |

## Code Comparison

### GET /todos - List All Todos

**Flask:**
```python
@app.route("/todos")
def get_all_todos():
    return jsonify({"todos": todos})
```

**FastAPI:**
```python
@app.get("/todos")
async def get_all_todos():
    return {"todos": todos}
```

**Key Differences:**
1. `@app.route()` → `@app.get()` (explicit HTTP method)
2. `jsonify()` not needed - FastAPI auto-converts dicts to JSON
3. `async def` is optional but recommended for FastAPI

### GET /todos/{id} - Get Single Todo

**Flask:**
```python
@app.route("/todos/<int:id>")
def get_todo_by_id(id):
    todo = find_todo_by_id(id)
    if todo:
        return jsonify({"todo": todo})
    else:
        return jsonify({"error": "Todo not found."}), 404
```

**FastAPI:**
```python
@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"todo": todo}
```

**Key Differences:**
1. Path parameter syntax: `<int:id>` → `{todo_id}`
2. Type hint: `todo_id: int` provides automatic validation
3. Error handling: `return ..., 404` → `raise HTTPException(...)`

## What We Gained

### 1. Automatic API Documentation
Visit http://localhost:8000/docs to see:
- All endpoints listed with descriptions
- Try it out buttons for testing
- Request/response examples

### 2. Automatic Validation
If someone calls `/todos/abc` (non-integer ID):
- **Flask**: Would crash or need manual handling
- **FastAPI**: Returns `422 Unprocessable Entity` with helpful error message

### 3. Better Error Messages
FastAPI validation errors include:
```json
{
  "detail": [
    {
      "loc": ["path", "todo_id"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

## Verification

### Test Commands

```bash
# Get all todos (empty list)
curl http://localhost:8000/todos
# Response: {"todos": []}

# Try to get non-existent todo
curl http://localhost:8000/todos/1
# Response: {"detail": "Todo not found"}

# Try invalid ID (non-integer)
curl http://localhost:8000/todos/abc
# Response: 422 with validation error
```

### Via Swagger UI
1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Click "Execute"
5. See the response

## Next Step

Proceed to **Phase 3: Web Interface Routes** to add the HTML pages.

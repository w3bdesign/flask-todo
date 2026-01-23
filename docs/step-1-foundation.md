# Step 1: Foundation Setup

This document explains the foundation files created for the FastAPI conversion.

## Files Created

### 1. `models.py` - Pydantic Data Models

**What it does:** Defines the structure of our todo data using Pydantic models.

**Flask vs FastAPI Comparison:**

```python
# Flask - Plain dictionaries (no validation)
todo = {"id": 1, "title": "Buy milk", "description": "2% milk"}

# FastAPI - Pydantic models (automatic validation)
todo = Todo(id=1, title="Buy milk", description="2% milk")
```

**Models we created:**

| Model | Purpose | Fields |
|-------|---------|--------|
| `TodoCreate` | Creating new todos | title, description |
| `TodoUpdate` | Updating existing todos | title (optional), description (optional) |
| `Todo` | Complete todo with ID | id, title, description |

**Why separate models?**
- `TodoCreate` has no `id` because the server generates it
- `TodoUpdate` has optional fields so you can update just the title or just the description
- `Todo` is the complete representation stored and returned

### 2. `main.py` - FastAPI Application

**What it does:** Sets up the FastAPI application with static files and templates.

**Key differences from Flask:**

| Aspect | Flask (`app.py`) | FastAPI (`main.py`) |
|--------|------------------|---------------------|
| Import | `from flask import Flask` | `from fastapi import FastAPI` |
| Create app | `app = Flask(__name__)` | `app = FastAPI()` |
| Static files | Automatic | `app.mount("/static", StaticFiles(...))` |
| Templates | Automatic | `templates = Jinja2Templates(...)` |
| Run server | `python app.py` | `uvicorn main:app --reload` |

**What's in main.py right now:**
- FastAPI app initialization with title and description
- Static files mounted at `/static`
- Jinja2 templates configured
- In-memory `todos` list (same as Flask)
- Helper functions: `generate_id()`, `find_todo_by_id()`
- A `/health` endpoint to verify the app works

### 3. `requirements.txt` - Dependencies

**New packages added:**

| Package | Purpose |
|---------|---------|
| `fastapi` | The web framework |
| `uvicorn[standard]` | ASGI server to run FastAPI |
| `python-multipart` | Required for form handling |
| `pydantic` | Data validation (included with FastAPI) |
| `pytest` | Testing framework |
| `httpx` | HTTP client for testing |

## How to Verify Phase 1

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the FastAPI server

```bash
uvicorn main:app --reload --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Test the endpoints

**Option A: Browser**
- Visit http://localhost:8000/docs - You should see Swagger UI
- Visit http://localhost:8000/health - You should see `{"status": "healthy"}`

**Option B: Command line**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "message": "FastAPI Todo App is running!"}
```

## What You Should See

### Swagger UI at `/docs`

When you visit http://localhost:8000/docs, you'll see:

1. **API Title**: "Todo App"
2. **Description**: "A simple todo application - converted from Flask to FastAPI"
3. **Endpoints listed**: Just `/health` for now
4. **"Try it out" button**: Click to test the endpoint directly

This automatic documentation is one of FastAPI's biggest advantages over Flask!

### Health Check Response

The `/health` endpoint confirms everything is working:
```json
{
  "status": "healthy",
  "message": "FastAPI Todo App is running!"
}
```

## Key Learning Points

1. **Pydantic models** provide type safety that Flask dictionaries don't have
2. **FastAPI requires explicit setup** for static files and templates (Flask does it automatically)
3. **uvicorn** is the server for FastAPI (like Flask's built-in server, but faster)
4. **Automatic API docs** are generated from your code - no extra work needed!

## Next Step

Proceed to **Phase 2: API Routes** to add the `/todos` endpoints.

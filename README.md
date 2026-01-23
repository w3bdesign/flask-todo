# FastAPI Todo App

A modern Todo application built with FastAPI and Tailwind CSS. Create, read, update, delete, and toggle completion status of your tasks with a clean, responsive interface.

## Features

- ✅ Add new tasks with optional descriptions
- ✅ Mark tasks as complete/incomplete with one click
- ✅ Edit tasks via modal dialog
- ✅ Delete tasks with confirmation
- ✅ Clean, minimal UI with Tailwind CSS
- ✅ Automatic API documentation (Swagger/ReDoc)

## Getting Started

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Open http://localhost:8000 in your browser

## API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface - displays all todos |
| `POST` | `/` | Create a new todo |
| `GET` | `/todos` | Get all todos (JSON) |
| `GET` | `/todos/{id}` | Get a specific todo (JSON) |
| `GET` | `/toggle/{id}` | Toggle completion status |
| `GET` | `/edit/{id}` | Edit form (GET) |
| `POST` | `/edit/{id}` | Update a todo |
| `GET` | `/delete/{id}` | Delete a todo |
| `GET` | `/health` | Health check endpoint |

## Project Structure

```
flask-todo/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── app.py               # Legacy Flask application
├── templates/
│   ├── index.html       # Main page with todo list and edit modal
│   └── edit.html        # Standalone edit page (legacy)
├── static/
│   └── css/
│       └── main.css     # Compiled Tailwind CSS
├── requirements.txt     # Python dependencies
└── README.md
```

## Tech Stack

- **Backend**: FastAPI with Pydantic for data validation
- **Frontend**: Jinja2 templates with Tailwind CSS (CDN)
- **Server**: Uvicorn ASGI server

## Credits

This app was created by Daniel Fjeldstad (w3bdesign).

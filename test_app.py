"""
FastAPI Todo Application Tests

This file demonstrates how to test a FastAPI application using pytest.

Flask vs FastAPI Testing Comparison:
------------------------------------
Flask:
    - Uses unittest.TestCase
    - Uses app.test_client()
    - Response data accessed via response.data

FastAPI:
    - Uses pytest (simpler, more Pythonic)
    - Uses TestClient from fastapi.testclient
    - Response data accessed via response.json() or response.text

Run tests:
    pytest test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app, todos


# =============================================================================
# Fixtures - Setup code that runs before each test
# =============================================================================

@pytest.fixture
def client():
    """
    Create a fresh test client for each test.
    
    The todos list is cleared to ensure each test starts with clean state.
    This is similar to Flask's setUp() method in unittest.TestCase.
    """
    todos.clear()
    return TestClient(app)


@pytest.fixture
def client_with_todo(client):
    """
    Create a test client with one pre-existing todo.
    
    Useful for testing edit, delete, and get operations.
    """
    client.post("/create", data={"title": "Existing Todo", "description": "Pre-created"})
    return client


# =============================================================================
# Web Interface Tests (HTML Forms)
# =============================================================================

def test_index_page_loads(client):
    """Test that the homepage loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text


def test_create_page_loads(client):
    """Test that the create form page loads."""
    response = client.get("/create")
    assert response.status_code == 200
    assert "Create new entry" in response.text


def test_create_todo(client):
    """
    Test creating a new todo via form submission.
    
    Flask equivalent:
        response = self.app.post("/create", data=dict(...), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    FastAPI difference:
        - Uses data= for form data (same as Flask)
        - follow_redirects=True to follow the 303 redirect
        - Uses assert instead of self.assertEqual
    """
    response = client.post(
        "/create",
        data={"title": "Test Todo", "description": "This is a test todo"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Test Todo" in response.text
    assert len(todos) == 1


def test_create_todo_returns_redirect(client):
    """Test that creating a todo returns a 303 See Other redirect."""
    response = client.post(
        "/create",
        data={"title": "Test Todo", "description": "Test"},
        follow_redirects=False  # Don't follow redirect
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_edit_page_loads(client_with_todo):
    """Test that the edit form loads for an existing todo."""
    response = client_with_todo.get("/edit/1")
    assert response.status_code == 200
    assert "Edit entry" in response.text
    assert "Existing Todo" in response.text


def test_edit_page_404_for_nonexistent(client):
    """Test that editing a non-existent todo returns 404."""
    response = client.get("/edit/999")
    assert response.status_code == 404


def test_edit_todo(client_with_todo):
    """Test updating an existing todo."""
    response = client_with_todo.post(
        "/edit/1",
        data={"title": "Updated Title", "description": "Updated Description"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Updated Title" in response.text
    # Verify the todo was actually updated
    assert todos[0].title == "Updated Title"


def test_delete_todo(client_with_todo):
    """Test deleting a todo."""
    assert len(todos) == 1
    response = client_with_todo.get("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert len(todos) == 0


def test_delete_nonexistent_todo(client):
    """Test that deleting a non-existent todo returns 404."""
    response = client.get("/delete/999")
    assert response.status_code == 404


# =============================================================================
# API Endpoint Tests (JSON)
# =============================================================================

def test_get_all_todos_empty(client):
    """Test getting todos when list is empty."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_todos_with_data(client_with_todo):
    """Test getting todos when list has items."""
    response = client_with_todo.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Existing Todo"


def test_get_single_todo(client_with_todo):
    """Test getting a single todo by ID."""
    response = client_with_todo.get("/todos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Existing Todo"


def test_get_single_todo_not_found(client):
    """Test getting a non-existent todo returns 404."""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_todo_invalid_id(client):
    """
    Test that an invalid ID (non-integer) returns 422.
    
    This is a FastAPI feature - automatic validation!
    Flask would either crash or need manual validation.
    """
    response = client.get("/todos/abc")
    assert response.status_code == 422  # Unprocessable Entity


# =============================================================================
# Health Check Test
# =============================================================================

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# =============================================================================
# Swagger/OpenAPI Documentation Tests
# =============================================================================

def test_swagger_docs_available(client):
    """Test that Swagger UI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


def test_redoc_available(client):
    """Test that ReDoc documentation is available."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_json(client):
    """Test that OpenAPI JSON schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "/todos" in data["paths"]


# =============================================================================
# Run tests directly (optional - pytest usually handles this)
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

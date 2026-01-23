"""
Pydantic Models for the Todo Application

This file defines the data models used throughout the FastAPI application.
Pydantic models provide automatic data validation and type safety.

Flask Comparison:
-----------------
In Flask, we used plain Python dictionaries:
    todo = {"id": 1, "title": "Sample", "description": "Description"}

In FastAPI, we use Pydantic models which provide type safety:
    todo = Todo(id=1, title="Sample", description="Description")
"""

from pydantic import BaseModel
from typing import Optional


class TodoCreate(BaseModel):
    """Model for creating a new todo item (no ID - server generates it)."""
    title: str
    description: str = ""
    completed: bool = False  # NEW: Track if todo is done


class TodoUpdate(BaseModel):
    """Model for updating a todo item (all fields optional)."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None  # NEW: Can update completed status


class Todo(BaseModel):
    """Complete todo item with ID."""
    id: int
    title: str
    description: str = ""
    completed: bool = False  # NEW: Default to not completed

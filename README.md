# Flask Todo App

A simple Flask app that allows you to create, read, update, and delete todo items. This app uses Flask for the backend, and HTML templates for the frontend.

## Getting Started

1.  Clone the repository.
2.  Install the required packages with `pip install -r requirements.txt`.
3.  Run the app with `python app.py`.

## API Endpoints

The following API endpoints are available:

### `GET /todos`

Returns a list of all todos.

### `GET /todos/<int:id>`

Returns the todo with the specified ID.

### `POST /create`

Creates a new todo item.

### `POST /edit/<int:id>`

Updates the todo item with the specified ID.

### `DELETE /delete/<int:id>`

Deletes the todo item with the specified ID.

## Code Overview

The app consists of the following files:

*   `app.py`: This file contains the main Flask application.
*   `templates/index.html`: This file contains the HTML template for the main page of the app.
*   `templates/create.html`: This file contains the HTML template for the create todo page.
*   `templates/edit.html`: This file contains the HTML template for the edit todo page.
*   `requirements.txt`: This file contains the required packages for the app.
*   `README.md`: This file contains information about the app.

## Usage

To use the app, simply navigate to `http://localhost:5000/` in your web browser. From there, you can create new todos, edit existing ones, and delete them.

## Credits

This app was created by Daniel Fjeldstad (w3bdesign).

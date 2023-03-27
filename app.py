from flask import Flask, render_template, request, redirect, make_response
import json

app = Flask(__name__)


@app.route("/")
def index():
    todos = get_todos()
    return render_template("index.html", todos=todos)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        return create_todo(
            {"id": generate_id(), "title": title, "description": description}
        )
    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        update_todo_by_id(id, {"title": title, "description": description})
        return redirect("/")
    return render_template("edit.html", todo=todo)


@app.route("/delete/<int:id>")
def delete(id):
    delete_todo_by_id(id)
    return redirect("/")


def get_todos():
    todos = json.loads(request.cookies.get("todos", "[]"))
    # If there are no todos in the cookie, check local storage
    if not todos:
        todos = json.loads(request.args.get("todos", "[]"))
    return todos


def generate_id():
    todos = get_todos()
    if not todos:
        return 1
    return max([todo["id"] for todo in todos]) + 1


def create_todo(todo):
    todos = get_todos()
    todos.append(todo)
    response = make_response(redirect("/"))
    response.set_cookie("todos", json.dumps(todos), samesite="None", secure=True)
    return response


def get_todo_by_id(id):
    todos = get_todos()
    for todo in todos:
        if todo["id"] == id:
            return todo
    return None


def update_todo_by_id(id, new_todo):
    todos = get_todos()
    for i in range(len(todos)):
        if todos[i]["id"] == id:
            todos[i] = new_todo
            response = make_response(redirect("/"))
            response.set_cookie("todos", json.dumps(todos))
            return response
    return None


def delete_todo_by_id(id):
    todos = get_todos()
    for i in range(len(todos)):
        if todos[i]["id"] == id:
            del todos[i]
            response = make_response(redirect("/"))
            response.set_cookie("todos", json.dumps(todos))
            return response
    return None

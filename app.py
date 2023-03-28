from flask import Flask, redirect, render_template, request, jsonify, url_for
import requests

app = Flask(__name__)

todos = []


@app.route("/")
def index():
    # Retrieve the todos from the /todos API endpoint
    response = requests.get("http://localhost:5000/todos")
    todos = response.json()["todos"]
    return render_template("index.html", todos=todos)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = {"id": generate_id(), "title": title, "description": description}
        create_todo(todo)
        return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        update_todo_by_id(id, {"title": title, "description": description})
        #return jsonify({"message": "Todo updated successfully."})
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)


@app.route("/delete/<int:id>")
def delete(id):
    delete_todo_by_id(id)
    #return jsonify({"message": "Todo deleted successfully."})
    return redirect(url_for("index"))


@app.route("/todos")
def get_all_todos():
    return jsonify({"todos": todos})


@app.route("/todos/<int:id>")
def get_todo_by_id(id):
    todo = None
    for t in todos:
        if t["id"] == id:
            todo = t
            break
    if todo:
        return jsonify({"todo": todo})
    else:
        return jsonify({"error": "Todo not found."}), 404


def generate_id():
    if not todos:
        return 1
    return max([todo["id"] for todo in todos]) + 1


def create_todo(todo):
    todos.append(todo)


def update_todo_by_id(id, new_todo):
    for i in range(len(todos)):
        if todos[i]["id"] == id:
            todos[i] = {**todos[i], **new_todo}
            return
    raise Exception("Todo not found.")


def delete_todo_by_id(id):
    for i in range(len(todos)):
        if todos[i]["id"] == id:
            del todos[i]
            return
    raise Exception("Todo not found.")

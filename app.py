from flask import Flask, redirect, render_template, request, jsonify, url_for
import requests

app = Flask(__name__)

todos = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        todo = {
            "id": generate_id(),
            "title": title,
            "description": description,
            "completed": False
        }
        create_todo(todo)
        return redirect(url_for("index"))
    return render_template("index.html", todos=todos)


@app.route("/toggle/<int:id>")
def toggle(id):
    toggle_todo_by_id(id)
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = find_todo_by_id(id)
    if not todo:
        return redirect(url_for("index"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        update_todo_by_id(id, {"title": title, "description": description})
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)


@app.route("/delete/<int:id>")
def delete(id):
    delete_todo_by_id(id)
    return redirect(url_for("index"))


@app.route("/todos")
def get_all_todos():
    return jsonify({"todos": todos})


@app.route("/todos/<int:id>")
def get_todo_by_id(id):
    todo = find_todo_by_id(id)
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


def find_todo_by_id(id):
    for t in todos:
        if t["id"] == id:
            return t
    return None


def toggle_todo_by_id(id):
    for i in range(len(todos)):
        if todos[i]["id"] == id:
            todos[i]["completed"] = not todos[i].get("completed", False)
            return
    raise Exception("Todo not found.")


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

if __name__ == "__main__":
    app.run(debug=False)

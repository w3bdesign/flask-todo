# Step 5: Testing Your FastAPI App

## 🎯 What You'll Learn

Testing might sound boring, but it's actually really useful! In this step, you'll learn:

- How to write tests for your FastAPI app
- The differences between Flask and FastAPI testing
- How to run tests and see if everything works

---

## 🤔 Why Write Tests?

Imagine you make a change to your code and accidentally break something. Tests catch these problems automatically!

```
You: "I just added a cool new feature!"
Tests: "🚨 Alert! Your delete function is broken!"
You: "Oh no, let me fix that..."
```

Without tests, you might not notice until a user complains!

---

## 📦 What You Need

Make sure you have these installed (they're in requirements.txt):

```bash
pip install pytest httpx
```

- **pytest** - Makes writing tests easy and fun
- **httpx** - Lets us send requests to our app during testing

---

## 🔄 Flask vs FastAPI Testing

### Flask Testing (the old way):
```python
import unittest
from app import app, todos

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_create_todo(self):
        response = self.app.post("/create", data={"title": "Test"})
        self.assertEqual(response.status_code, 200)
```

### FastAPI Testing (the new way):
```python
import pytest
from fastapi.testclient import TestClient
from main import app, todos

@pytest.fixture
def client():
    todos.clear()
    return TestClient(app)

def test_create_todo(client):
    response = client.post("/create", data={"title": "Test"})
    assert response.status_code == 303
```

**What's different?**
- No more `class` and `self` everywhere!
- `assert` instead of `self.assertEqual()` - much cleaner!
- Uses `@pytest.fixture` to set things up

---

## 📝 Writing Your First Test

Let's break down a simple test:

```python
def test_homepage_loads(client):
    # Step 1: Make a request
    response = client.get("/")
    
    # Step 2: Check if it worked
    assert response.status_code == 200
    
    # Step 3: Check the content
    assert "Todo List" in response.text
```

That's it! Three simple steps:
1. **Do something** (visit a page)
2. **Check the result** (was it successful?)
3. **Verify the content** (is it what we expected?)

---

## 🧩 Understanding Fixtures

A **fixture** is code that runs before each test to set things up:

```python
@pytest.fixture
def client():
    todos.clear()  # Start fresh every time
    return TestClient(app)
```

**Why clear the todos?** 

Each test should start with a clean slate. If one test adds a todo, we don't want it affecting other tests!

Think of it like cleaning the kitchen before cooking - you want to start fresh each time.

---

## 📋 Test Examples

Here are some tests you might write:

### Test 1: Homepage loads correctly
```python
def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text
```

### Test 2: Create a new todo
```python
def test_create_todo(client):
    response = client.post(
        "/create",
        data={"title": "Buy groceries", "description": "Milk and bread"}
    )
    # 303 means "redirect after POST" - that's good!
    assert response.status_code == 303
```

### Test 3: Todo appears after creation
```python
def test_todo_appears_after_creation(client):
    # Create a todo
    client.post("/create", data={"title": "Test Todo", "description": ""})
    
    # Check the homepage
    response = client.get("/")
    assert "Test Todo" in response.text
```

### Test 4: Edit a todo
```python
def test_edit_todo(client):
    # First create a todo
    client.post("/create", data={"title": "Original", "description": ""})
    
    # Then edit it
    response = client.post(
        "/edit/1",
        data={"title": "Updated Title", "description": "New description"}
    )
    assert response.status_code == 303
```

### Test 5: Delete a todo
```python
def test_delete_todo(client):
    # Create a todo
    client.post("/create", data={"title": "To Delete", "description": ""})
    
    # Delete it
    response = client.get("/delete/1")
    assert response.status_code == 303
    
    # Check it's gone
    response = client.get("/")
    assert "To Delete" not in response.text
```

### Test 6: 404 for non-existent todo
```python
def test_get_nonexistent_todo(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
```

---

## ▶️ Running Your Tests

Open your terminal and run:

```bash
pytest test_app.py -v
```

The `-v` means "verbose" - it shows you more details.

### What You Should See:

```
test_app.py::test_homepage_loads PASSED
test_app.py::test_create_todo PASSED
test_app.py::test_edit_todo PASSED
test_app.py::test_delete_todo PASSED
...

========== 18 passed in 1.60s ==========
```

**All green? 🎉 Your app works!**

---

## 🔴 What If a Test Fails?

Don't panic! A failed test looks like this:

```
test_app.py::test_homepage_loads FAILED

    def test_homepage_loads(client):
        response = client.get("/")
>       assert response.status_code == 200
E       assert 500 == 200

FAILED test_app.py::test_homepage_loads
```

This tells you:
1. **Which test failed** - `test_homepage_loads`
2. **What went wrong** - Expected 200, got 500
3. **Where to look** - The `>` shows the exact line

---

## 🎨 Test Tips for Beginners

### Tip 1: Give tests descriptive names
```python
# ❌ Bad
def test_1(client):
    ...

# ✅ Good
def test_creating_todo_redirects_to_homepage(client):
    ...
```

### Tip 2: Test one thing at a time
```python
# ❌ Bad - testing too many things
def test_everything(client):
    response = client.get("/")
    assert response.status_code == 200
    response = client.post("/create", data={"title": "Test"})
    assert response.status_code == 303
    # ... 50 more lines

# ✅ Good - one concept per test
def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_redirects(client):
    response = client.post("/create", data={"title": "Test"})
    assert response.status_code == 303
```

### Tip 3: Run tests often
After every change you make, run:
```bash
pytest test_app.py -v
```

---

## 🎓 Quick Reference

| What You Want | How to Do It |
|---------------|--------------|
| Make a GET request | `client.get("/path")` |
| Make a POST request | `client.post("/path", data={...})` |
| Check status code | `assert response.status_code == 200` |
| Check page content | `assert "text" in response.text` |
| Check JSON response | `assert response.json() == {...}` |
| Follow redirects | `client.get("/path", follow_redirects=True)` |

---

## 🏆 Challenge: Write Your Own Test!

Try writing a test that:
1. Creates a todo called "Learn Testing"
2. Checks that it appears on the homepage
3. Deletes it
4. Checks that it's gone

<details>
<summary>Click to see the answer</summary>

```python
def test_create_and_delete_todo(client):
    # Create
    client.post("/create", data={"title": "Learn Testing", "description": ""})
    
    # Check it exists
    response = client.get("/")
    assert "Learn Testing" in response.text
    
    # Delete
    client.get("/delete/1")
    
    # Check it's gone
    response = client.get("/")
    assert "Learn Testing" not in response.text
```
</details>

---

## ⏭️ What's Next?

Congratulations! 🎉 In **Step 6**, we'll wrap everything up and make sure your conversion is complete.

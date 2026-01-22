import unittest
from app import app, todos


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_create_todo(self):
        response = self.app.post(
            "/create",
            data=dict(title="Test Todo", description="This is a test todo"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        todos.clear()


if __name__ == "__main__":
    unittest.main()

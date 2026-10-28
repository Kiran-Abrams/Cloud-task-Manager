

import unittest
from unittest.mock import patch

from app.app import app


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task Manager", response.data)

    def test_create_task_requires_title(self):
        response = self.client.post(
            "/api/tasks",
            json={"title": "   ", "description": "No title"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_task_rejects_long_title(self):
        response = self.client.post(
            "/api/tasks",
            json={"title": "x" * 201},
        )
        self.assertEqual(response.status_code, 400)

    @patch("app.app.cache.ping")
    @patch("app.app.get_db_connection")
    def test_health_check(self, mock_db_connection, mock_cache_ping):
        mock_connection = mock_db_connection.return_value
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_connection.cursor.return_value

        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")
        mock_cache_ping.assert_called_once()


if __name__ == "__main__":
    unittest.main()

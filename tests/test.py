
import unittest
from app.app import app


class TestCloudTaskManagerAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"message": "Cloud Task Manager API is running!"}
        )

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"status": "healthy"}
        )


if __name__ == "__main__":
    unittest.main()

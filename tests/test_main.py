import unittest

from fastapi.testclient import TestClient

from src import main


class TestTranslate(unittest.TestCase):
    def setUp(self):
        self.app = main.app
        self.client = TestClient(self.app)

    def test_root_success(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("swagger", response.text)

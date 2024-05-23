import unittest
from unittest import mock
from fastapi import APIRouter
from fastapi.testclient import TestClient
from src import main


class TestTranslate(unittest.TestCase):
    def setUp(self):
        self.app = main.app
        router = APIRouter()
        self.app.include_router(router)
        self.client = TestClient(self.app)

        self.mock_service_patcher = mock.patch('src.translator.tasks.translate_external_api')
        self.mock_translate_external_api = self.mock_service_patcher.start()

    def tearDown(self):
        self.mock_service_patcher.stop()  # Make sure to stop the patching after each test.

    def test_translate_successful_translation(self):
        # Mock the response value here
        self.mock_translate_external_api.return_value = "Hola"
        response = self.client.post("/translate", json={"text": "Hello", "languages": ["es", "fr"]})
        self.assertEqual(response.status_code, 200)

        # Make sure translate_external_api was called with the correct arguments
        self.mock_translate_external_api.assert_any_call("Hello", "es")
        self.mock_translate_external_api.assert_any_call("Hello", "fr")
        assert self.mock_translate_external_api.call_count == 2

    def test_translate_with_empty_languages(self):
        response = self.client.post("/translate", json={"text": "Hello", "languages": []})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_translate_with_non_list_languages(self):
        response = self.client.post("/translate", json={"text": "Hello", "languages": "es"})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_translate_without_text(self):
        response = self.client.post("/translate", json={"languages": ["es", "fr"]})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

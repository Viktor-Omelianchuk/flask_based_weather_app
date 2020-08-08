import pytest
from flask_based_weather_app.flask_based_weather_app import app


class TestViews:

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_get(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_home_post(self):
        response = self.client.post('/')
        assert response.status_code == 302

    def test_home_put(self):
        response = self.client.put('/')
        assert response.status_code == 405

    def teardown(self):
        pass

from flask_based_weather_app.flask_based_weather_app import get_weather_date


class TestViews:

    def test_get_weather_date(self):
        city = 'Rivne'
        response = get_weather_date(city)
        print(type(response))
        assert response['cod'] == 200
        assert 'temp' in response['main']
        assert 'description' in response["weather"][0]
        assert 'icon' in response["weather"][0]

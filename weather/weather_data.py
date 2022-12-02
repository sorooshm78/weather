import requests
from requests.exceptions import ConnectionError

from django.conf import settings


class WeatherData:
    def __init__(self, city_name):
        self.city_name = city_name
        self.api_key = settings.API_KEY
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric"

    def get_data(self):
        try:
            response = requests.get(self.url)
        except ConnectionError:
            raise Exception("Connection Error")
        else:
            if response.status_code != 200:
                raise Exception("City Not Exist")

            return response.json()

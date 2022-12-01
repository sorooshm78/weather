import requests
from requests.exceptions import ConnectionError

from django.conf import settings


class WeatherData:
    def __init__(self, city_name):
        self.city_name = city_name
        self.api_key = settings.API_KEY
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric"

    def city_exist(self):
        try:
            response = requests.get(self.url)
        except ConnectionError:
            raise Exception("Connection Error")
        else:
            if response.status_code != 200:
                raise Exception("City Not Exist")

    def __get_json_data(self):
        response = requests.get(self.url)
        return response.json()

    def get_weather_data(self):
        try:
            data = self.__get_json_data()
            return {
                "city": self.city_name,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        except ConnectionError:
            err = "Connection Error"
            return {
                "city": self.city_name,
                "temperature": 0,
                "description": err,
            }

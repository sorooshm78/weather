import requests
import json

from django.views.generic import CreateView, DeleteView
from django.urls import reverse

from .models import City
from .forms import CityModelForm


class CityWeatherData:
    def __init__(self, city_name):
        self.city_name = city_name
        self.api_key = self.get_api_key()
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"

    def get_api_key(self):
        with open("secret.json", "r") as secret_file:
            api_key = json.load(secret_file)["Key"]
        return api_key

    def city_exist(self):
        try:
            response = requests.get(self.url)
        except BaseException:
            raise ValueError("Connection Error")
        else:
            if response.status_code != 200:
                raise ValueError("City Not Exist")

    def get_json_data(self):
        response = requests.get(self.url)
        return response.json()

    def get_data(self):
        try:
            data = self.get_json_data()
            return {
                "city": self.city_name,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        except BaseException:
            err = "Connection Error"
            return {
                "city": self.city_name,
                "temperature": 0,
                "description": err,
            }


# Create your views here.
class ListCreateCityView(CreateView):
    model = City
    form_class = CityModelForm
    template_name = "weather/weather.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_data = []
        for city in self.get_queryset():
            weather_data.append(CityWeatherData(city.name).get_data())

        context["weather_data"] = weather_data
        return context

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        city_name = form.cleaned_data["name"]

        try:
            CityWeatherData(city_name).city_exist()
            return super().form_valid(form)
        except ValueError as err:
            form.add_error("name", err)
            return self.form_invalid(form)


class DeleteCity(DeleteView):
    model = City
    slug_field = "name"
    slug_url_kwarg = "city_name"

    def get_success_url(self):
        return reverse("index")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

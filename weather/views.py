import requests
import json

from django.views.generic import CreateView, DeleteView
from django.urls import reverse

from .models import City
from .forms import CityModelForm

# Create your views here.
class ListCreateCityView(CreateView):
    model = City
    form_class = CityModelForm
    template_name = "weather/weather.html"

    def __init__(self, *args, **kwargs):
        self.api_key = self.get_api_key()

    def get_url(self, city_name):
        url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        return url.format(city_name=city_name, api_key=self.api_key)

    def get_api_key(self):
        with open("secret.json", "r") as secret_file:
            api_key = json.load(secret_file)["Key"]
        return api_key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_data = []
        for city in self.get_queryset():
            response = requests.get(self.get_url(city.name)).json()
            weather_data.append(
                {
                    "city": city.name,
                    "temperature": response["main"]["temp"],
                    "description": response["weather"][0]["description"],
                    "icon": response["weather"][0]["icon"],
                }
            )
        context["weather_data"] = weather_data
        return context

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        city_name = form.cleaned_data["name"]
        response = requests.get(self.get_url(city_name))

        if response.status_code != 200:
            form.add_error("name", "City is not exist")
            return self.form_invalid(form)

        return super().form_valid(form)


class DeleteCity(DeleteView):
    model = City
    slug_field = "name"
    slug_url_kwarg = "city_name"

    def get_success_url(self):
        return reverse("index")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

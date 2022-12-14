from concurrent.futures import ThreadPoolExecutor

from django.views.generic import CreateView, DeleteView
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache

from .models import City
from .forms import CityModelForm
from .weather_data import WeatherData


class ListCreateCityView(CreateView):
    model = City
    form_class = CityModelForm
    template_name = "weather/weather.html"

    def __init__(self):
        self.MAX_THREAD_WORKERS = settings.MAX_THREAD_WORKERS
        self.CACHE_TTL = settings.CACHE_TTL

    def prepare_data(self, city_name):
        data = WeatherData(city_name).get_data()
        city_weather_data = {
            "city": city_name,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        cache.set(city_name, city_weather_data, self.CACHE_TTL)
        return city_weather_data

    def get_city_weather_data(self, city_name):
        try:
            cache_city_weather_data = cache.get(city_name)
            if cache_city_weather_data is not None:
                return cache_city_weather_data

            return self.prepare_data(city_name)

        except Exception as err:
            return {
                "city": city_name,
                "temperature": 0,
                "description": err,
            }

    def get_context_weather_data(self, list_city):
        with ThreadPoolExecutor(max_workers=self.MAX_THREAD_WORKERS) as pool:
            weather_data = list(pool.map(self.get_city_weather_data, list_city))

        return weather_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_city = self.get_queryset()
        context["weather_data"] = self.get_context_weather_data(list_city)

        return context

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        city_name = form.cleaned_data["name"]

        try:
            self.prepare_data(city_name)
            return super().form_valid(form)
        except Exception as err:
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

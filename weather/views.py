from django.views.generic import CreateView, DeleteView
from django.urls import reverse

from .models import City
from .forms import CityModelForm
from .weather_data import WeatherData


# Create your views here.
class ListCreateCityView(CreateView):
    model = City
    form_class = CityModelForm
    template_name = "weather/weather.html"

    def get_city_weather_data(self, city_name):
        try:
            data = WeatherData(city_name).get_data()
            return {
                "city": city_name,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        except Exception as err:
            return {
                "city": city_name,
                "temperature": 0,
                "description": err,
            }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_data = []
        for city in self.get_queryset():
            weather_data.append(self.get_city_weather_data(city.name))

        context["weather_data"] = weather_data
        return context

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        city_name = form.cleaned_data["name"]

        try:
            WeatherData(city_name).get_data()
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

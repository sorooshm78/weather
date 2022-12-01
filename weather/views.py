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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_data = []
        for city in self.get_queryset():
            weather_data.append(WeatherData(city.name).get_weather_data())

        context["weather_data"] = weather_data
        return context

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        city_name = form.cleaned_data["name"]

        try:
            WeatherData(city_name).city_exist()
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

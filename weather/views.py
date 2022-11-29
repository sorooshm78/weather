import requests
import json

from django.views.generic import ListView, CreateView
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

    def get_api_key(self):
        with open("secret.json", "r") as secret_file:
            api_key = json.load(secret_file)["Key"]
        return api_key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # response = requests.get()
        for city in self.get_queryset():
            print(city.name)

        return context
    
    def get_success_url(self):
        return reverse('index')

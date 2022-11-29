from django.views.generic import TemplateView

# Create your views here.
class Home(TemplateView):
    template_name = "weather/weather.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weather_data"] = [
            {
                "icon": "o",
                "city": "tehran",
                "temperature": 45,
                "description": "tttt",
            },
        ]
        return context

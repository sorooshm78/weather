from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateCityView.as_view(), name="index"),
]

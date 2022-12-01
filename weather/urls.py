from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateCityView.as_view(), name="index"),
    path("delete/<city_name>/", views.DeleteCity.as_view(), name="delete_city"),
    # path("delete/<name>/", views.DeleteCity.as_view(), name="delete_city"),
]

from django import forms

from .models import City


class CityModelForm(forms.ModelForm):
    class Meta:
        model = City
        fields = [
            "name",
        ]

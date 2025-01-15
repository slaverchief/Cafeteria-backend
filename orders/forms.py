from django.forms.models import ModelForm
from django import forms
from .models import Order


class OrderCreateForm(ModelForm):


    class Meta:
        model = Order
        fields = "__all__"
        labels = {
            "table_number": "Номер стола",
            "items": "Блюда",
            "status": "Статус"
        }
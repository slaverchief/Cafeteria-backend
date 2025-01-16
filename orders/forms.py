from django.forms.models import ModelForm
from django import forms
from .models import Order, STATUS_CHOICES


class OrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = "__all__"
        labels = {
            "table_number": "Номер стола",
            "items": "Блюда",
            "status": "Статус"
        }

class OrderEditForm(ModelForm):

    class Meta:
        model = Order
        fields = ["items", "status"]
        labels = {
            "items": "Блюда",
            "status": "Статус"
        }
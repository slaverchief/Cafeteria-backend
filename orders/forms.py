from django.forms.models import ModelForm
from django import forms
from .models import Order, STATUS_CHOICES


class OrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'items']
        labels = {
            "table_number": "Номер стола",
            "items": "Блюда"
        }

class OrderEditForm(ModelForm):

    class Meta:
        model = Order
        fields = ["items", "status"]
        labels = {
            "items": "Блюда",
            "status": "Статус"
        }
from datetime import datetime
from random import choices

from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}₽"

    class Meta:
        verbose_name_plural = "Dishes"

STATUS_CHOICES =(
    (1, "Готово"),
    (2, "Оплачено"),
    (3, "В ожидании"),
)

class Order(models.Model):
    table_number = models.IntegerField(unique=True)
    items = models.ManyToManyField(Dish, related_name='orders')
    status = models.IntegerField(choices=STATUS_CHOICES, blank=False, default=3)
    paid_date = models.DateField(null=True, blank=True)


    def get_status(self):
        return STATUS_CHOICES[self.status-1][1]

    def total_price(self, as_int=False):
        s = sum([item.price for item in self.items.all()])
        if as_int:
            return s
        return str(s)+'₽'

    def get_items_list(self):
        string = ""
        items_list = self.items.all()
        for i, item in enumerate(items_list):
            string += f"{item.name}({item.price}₽)"
            if i != len(items_list) - 1:
                string += ', '
        return string
from random import choices

from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()

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
    total_price = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)

from django.test import TestCase
from orders import models
from datetime import datetime
from rest_framework.test import APITestCase


def init_db():
    dishes = [models.Dish.objects.create(name=f'TESTDISH{i}', price=100 + i * 50) for i in range(1, 6)]
    models.Order.objects.create(table_number=1, status=1, paid_date=datetime(2025, 1, 16)).items.add(*dishes)
    models.Order.objects.create(table_number=2, status=2)
    models.Order.objects.create(table_number=3, status=3).items.add(*dishes[1:3])
    models.Order.objects.create(table_number=4, status=2)
    models.Order.objects.create(table_number=5, status=1, paid_date=datetime(2025, 1, 16)).items.add(dishes[0])

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        init_db()

class BaseAPITestCase(APITestCase):
    @classmethod
    def setUp(cls):
        init_db()
import json

from apps.orders.models import Order, Dish
from apps.tests.base import BaseAPITestCase
from django.urls import reverse
from apps.orders import models

URL_edit = reverse("api_edit")
URL_read = reverse('api_retrieve')

class TestGET(BaseAPITestCase):

    def test_no_items_queries(self):
        resp1 = self.client.post(URL_read, {'status': 12212}, format='json')
        resp2 = self.client.post(URL_read, {'status': 3}, format='json')
        resp3 = self.client.post(URL_read, {"status": 1, 'table_number': Order.objects.filter().first().pk}, format='json')
        resp4 = self.client.post(URL_read, {'paid_date': '2025-01-16'}, format='json')
        resp5 = self.client.post(URL_read, {'paid_date': '11112222'}, format='json')
        resp6 = self.client.get(URL_read)
        self.assertEqual(resp1.status_code, 404)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(resp5.status_code, 400)
        self.assertEqual(resp6.status_code, 200)

    def test_with_items_queries(self):
        pks = [obj.pk for obj in Dish.objects.all()]
        resp1 = self.client.post(URL_read, {'items': [pks[0],pks[1]]}, format='json')
        resp2 = self.client.post(URL_read, {'items': [pks[2]], "status": 2}, format='json')
        resp3 = self.client.post(URL_read, {'items': [pks[0], pks[3]], 'status': 12123}, format='json')
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 404)
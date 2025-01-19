from tests.base import BaseTestCase
from django.urls import reverse
from orders import models


class TestOrderList(BaseTestCase):

    def test_200_code(self):
        response1 = self.client.get(reverse("list")+'?status=5')
        response2 = self.client.get(reverse("list") + '?status=1')
        response3 = self.client.get(reverse("list") + '?status=2')
        response4 = self.client.get(reverse("list") + '?status=3')
        response5 = self.client.get(reverse("list") + '?status=1021')
        response6 = self.client.get(reverse("list") + '?status=5&tn=212sasa1')
        response7 = self.client.get(reverse("list") + '?status=5&tn=3asas4')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response7.status_code, 200)

class TestOrderCreate(BaseTestCase):

    def test_200_code(self):
        dpks = [obj.pk for obj in models.Dish.objects.all()]
        response2 = self.client.post(reverse("create"), data={"table_number": "12",
                                                              "items": [dpks[0], dpks[1]]
                                                              })
        response3 = self.client.post(reverse("create"), data={"table_number": "1223",
                                                              "items": [dpks[0]]
                                                              })
        response4 = self.client.post(reverse("create"), data={"table_number": "121",
                                                              "items": [dpks[0], dpks[1], dpks[2]]
                                                              })
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)
        self.assertEqual(response4.status_code, 302)

class TestOrderUpdate(BaseTestCase):

    def test_200_code(self):
        pks = [obj.pk for obj in models.Order.objects.all()[:3]]
        dpks = [obj.pk for obj in models.Dish.objects.all()]
        response2 = self.client.post(reverse("edit", args=[pks[0]]), data={"status": "1",
                                                              "items": [dpks[0], dpks[1]]
                                                              })
        response3 = self.client.post(reverse("edit", args=[pks[1]]), data={"status": "2",
                                                              "items": [dpks[3]]
                                                              })
        response4 = self.client .post(reverse("edit", args=[pks[2]]), data={"status": "3",
                                                              "items": [dpks[3], dpks[0], dpks[1]]
                                                              })
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)
        self.assertEqual(response4.status_code, 302)

class TestOrderDelete(BaseTestCase):

    def test_200_code(self):
        pks = [obj.pk for obj in models.Order.objects.all()]
        response1 = self.client.get(reverse('delete', args=[pks[0]]))
        response2 = self.client.get(reverse('delete', args=[pks[2]]))
        self.assertLogs(response1.status_code, 200)
        self.assertLogs(response2.status_code, 200)
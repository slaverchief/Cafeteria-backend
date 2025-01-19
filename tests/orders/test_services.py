from orders.services.edit_services import set_paid_date
from orders.services.get_services import calculate_cash_sum
from tests.base import BaseTestCase
from orders import models
from datetime import datetime



class TestCashSumCalc(BaseTestCase):

    def test_total_cash(self):
        c1 = calculate_cash_sum(datetime(2025, 1, 15), datetime(2025, 1, 16))
        c2 = calculate_cash_sum(datetime(2025, 1, 14), datetime(2025, 1, 16))
        c3 = calculate_cash_sum(datetime(2022, 1, 14), datetime(2024, 1, 16))
        c4 = calculate_cash_sum(datetime(2025, 1, 12), datetime(2025, 1, 13))
        self.assertEqual(c1, 1400)
        self.assertEqual(c2, 1400)
        self.assertEqual(c3, 0)
        self.assertEqual(c4, 0)

class TestSetPaidDate(BaseTestCase):

    def test_paid_date_removal(self):
        order = models.Order.objects.filter(status=1).first()
        status_before = order.status
        order.status = 3
        status_after = order.status
        set_paid_date(status_before, status_after, order)
        self.assertEqual(order.paid_date, None)

    def test_paid_date_set_now(self):
        order = models.Order.objects.filter(status=3).first()
        status_before = order.status
        order.status = 1
        status_after = order.status
        set_paid_date(status_before, status_after, order)
        self.assertEqual(order.paid_date.strftime("%y%m%d"), datetime.now().strftime("%y%m%d"))
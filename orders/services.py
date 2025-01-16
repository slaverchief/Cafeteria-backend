from .models import Order

def calculate_cash_sum(from_date, to_date):
    return sum([int(n.total_price(as_int=True)) for n in Order.objects.filter(status__lte=2,
                                                              paid_date__gte=from_date,
                                                              paid_date__lte=to_date)])
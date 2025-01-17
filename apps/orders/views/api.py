from apps.cafeteria.base_api import BaseCafeteriaApiView
from serializers.orders import OrderSerializer
from apps.orders.models import Order

class OrderApiView(BaseCafeteriaApiView):
    Serializer = OrderSerializer
    Model = Order
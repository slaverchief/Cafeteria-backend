from .base import BaseCafeteriaSerializer
from apps.orders.models import Order

class OrderSerializer(BaseCafeteriaSerializer):

    class Meta:
        model = Order
        fields = '__all__'
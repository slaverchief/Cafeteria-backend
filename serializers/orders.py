from .base import BaseCafeteriaSerializer
from apps.orders.models import Order

# Сериалайзер для модели Order
class OrderSerializer(BaseCafeteriaSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 2
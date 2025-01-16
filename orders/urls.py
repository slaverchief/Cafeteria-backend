
from .views import *
from django.urls import path

urlpatterns = [
    path('list', OrdersListView.as_view(), name='list'),
    path("create", CreateOrderView.as_view(), name='create'),
    path("edit/<int:pk>", UpdateOrderView.as_view(), name='edit'),
    path('delete/<int:pk>', delete_order, name='delete')
]

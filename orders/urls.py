
from .views import *
from django.urls import path

urlpatterns = [
    path('list', OrdersListView.as_view())
]

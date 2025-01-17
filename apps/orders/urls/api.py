from django.urls.conf import path
from apps.orders.views.api import *

urlpatterns = [
    path('order', OrderApiView.as_view())
]
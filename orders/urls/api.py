from django.urls.conf import path
from orders.views.api import *

urlpatterns = [
    path('', OrderApiView.as_view(), name='api_edit'),
    path('retrieve', ReadOrderApiView.as_view(), name='api_retrieve'),
    path('cash', OrdersCashApiView.as_view(), name='api_getcash')
]
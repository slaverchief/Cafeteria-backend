from django.urls.conf import path
from apps.orders.views.api import *

urlpatterns = [
    path('', OrderApiView.as_view(), name='api_edit'),
    path('retrieve', ReadOrderApiView.as_view(), name='api_retrieve' )
]
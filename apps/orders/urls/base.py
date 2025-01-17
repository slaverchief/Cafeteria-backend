from django.urls.conf import path, include


urlpatterns = [
    path('api/', include('orders.urls.api')),
    path('', include('orders.urls.pages') )
]

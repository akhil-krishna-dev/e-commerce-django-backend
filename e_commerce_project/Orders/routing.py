from django.urls import path
from . import consumers  



websocket_urlpatterns = [
    path(r'ws/order-updates/<int:user_id>/', consumers.OrderUpdate.as_asgi()),
]
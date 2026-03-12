from django.urls import path
from .views import create_order, update_status

urlpatterns = [
    path("create-order/<int:product_id>/", create_order),
    path("update-status/<int:order_id>/", update_status, name="update-status"),
    
]
from django.shortcuts import redirect
from .models import Order
from accounts.models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request, product_id):

    product = Product.objects.get(id=product_id)
    print('product page')

    order = Order.objects.create(
        customer=request.user,
        product=product,
        status="CREATED"
    )

    return Response({
        "order_id": order.id,
        "status": order.status
    })


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_status(request, order_id):

    status = request.data.get("status")

    order = Order.objects.get(id=order_id)

    order.status = status
    order.save()

    # WebSocket event
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"order_{order.id}",
        {
            "type": "order_update",
            "order_id": order.id,
            "status": order.status
        }
    )

    return Response({
        "message": "status updated",
        "status": order.status
    })
from django.shortcuts import render
from asgiref.sync import async_to_sync
from .models import notification
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

channel_layer= get_channel_layer()

# Create your views here.
def notify_user(user, message):
    print("user notification -----------------------")
    notification.objects.create(user=user, message=message )

        # Send realtime
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": message
        }
    )

def notify_admins(message):
    print("admin notification ----------------------")
    admins = User.objects.filter(profile__role="ADMIN")

    for admin in admins:
        notification.objects.create(
            user=admin,
            message=message
        )

    async_to_sync(channel_layer.group_send)(
        "admins",
        {
            "type": "send_notification",
            "message": message
        }
    )



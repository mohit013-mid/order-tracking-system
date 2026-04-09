from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import notification


# def notification_list(request):
#     # Show user-specific notifications
#     print("----------------------------------------------------",request.user)
#     notifications = notification.objects.filter(user=request.user).order_by('-created_at')

#     # Mark all as read (optional auto-read)
#     if request.GET.get('mark_all') == 'true':
#         notifications.update(is_read=True)
#         return redirect('notifications')

#     return render(request, 'notification.html', {
#         'notifications': notifications
#     })
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_api(request):
    notifications = notification.objects.filter(user=request.user).order_by('-created_at')

    data = [
        {
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ]

    return Response(data)


# def mark_as_read(request, id):
#     notif = get_object_or_404(notification, id=id, user=request.user)
#     notif.is_read = True
#     notif.save()
#     return redirect('notifications')

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_as_read(request, id):
    notif = get_object_or_404(notification, id=id, user=request.user)
    notif.is_read = True
    notif.save()
    return Response({"message": "Marked as read"})

# ✅ Mark ALL notifications as read
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({"message": "All marked as read"})

def notification_list(request):

    return render(request, "notification.html")

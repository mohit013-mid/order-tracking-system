from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import notification


@login_required
def notification_list(request):
    # Show user-specific notifications
    print("----------------------------------------------------",request.user)
    notifications = notification.objects.filter(user=request.user).order_by('-created_at')

    # Mark all as read (optional auto-read)
    if request.GET.get('mark_all') == 'true':
        notifications.update(is_read=True)
        return redirect('notifications')

    return render(request, 'notification.html', {
        'notifications': notifications
    })


@login_required
def mark_as_read(request, id):
    notif = get_object_or_404(notification, id=id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')
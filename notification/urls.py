from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notification_list, name='notifications'),
    path('notifications_api/', views.notification_api, name='notifications'),
    path('notifications/read/<int:id>/', views.mark_as_read, name='mark_as_read'),
    path("api/notification/<int:id>/mark-read/", views.mark_as_read),
    path("api/notification/mark-all-read/", views.mark_all_read),
] 
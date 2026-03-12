from django.db import models
from django.contrib.auth.models import User
from accounts.models import Product

from django.db import models
from django.contrib.auth.models import User
from accounts.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("CREATED", "CREATED"),
        ("PACKED", "PACKED"),
        ("SHIPPED", "SHIPPED"),
        ("OUT_FOR_DELIVERY", "OUT_FOR_DELIVERY"),
        ("DELIVERED", "DELIVERED"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="CREATED")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderAssignment(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)

    assigned_at = models.DateTimeField(auto_now_add=True)
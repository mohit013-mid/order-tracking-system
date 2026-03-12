from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    ROLE_CHOICES = (
        ("ADMIN","ADMIN"),
        ("CUSTOMER","CUSTOMER"),
        ("AGENT","AGENT"),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
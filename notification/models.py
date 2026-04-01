from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    is_for_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.message

    










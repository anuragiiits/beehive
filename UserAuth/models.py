from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customuser')
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return "username: " + self.user.username + "  ||  is manager:   " + str(
            self.is_manager) + "   ||  is admin:  " + str(self.is_admin)

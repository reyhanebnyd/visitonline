from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(null=False, default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True) 
    def __str__(self):
        return self.user.username
    


from django.db import models
from django.contrib.auth.models import User
import pyotp

class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(null=False, default=False)
    otp_secret = models.CharField(max_length=16, default=pyotp.random_base32)

    def __str__(self):
        return self.user.username

    # Method to generate OTP
    def generate_otp(self):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()
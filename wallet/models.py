from django.db import models
from user.models import Appuser


class Wallet(models.Model):
    uid = models.OneToOneField(
        Appuser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
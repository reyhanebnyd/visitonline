from django.db import models


class Doctor(models.Model):
    career = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    accessdate = models.JSONField()
    avg_visit_time = models.DecimalField(max_digits=5, decimal_places=2)


class Fulltimes(models.Model):
    id_U = models.OneToOneField(
        'user.Appuser',
        on_delete=models.CASCADE,
    )
    id_D = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
    )
    accessdate = models.DateTimeField()
    paid = models.BooleanField(default=False)
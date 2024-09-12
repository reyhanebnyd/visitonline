from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    career = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    accessdate = models.JSONField()
    avg_visit_time = models.DecimalField(max_digits=5, decimal_places=2)


class Fulltimes(models.Model):
    id_U = models.ForeignKey(
        'user.Appuser',
        on_delete=models.CASCADE,
    )
    id_D = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
    )
    accessdate = models.DateTimeField()
    
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(null=False, default=False)


class Comments(models.Model):
    id_U = models.ForeignKey(
        Appuser,
        on_delete=models.CASCADE,
    )
    id_D = models.ForeignKey(
        'doctor.Doctor',
        on_delete=models.CASCADE,
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    context = models.CharField(max_length=255)
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
        related_name='uidcomments'
    )
    id_D = models.ForeignKey(
        'doctor.Doctor',
        on_delete=models.CASCADE,
        related_name='didcomments'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    context = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.context[:30]}'
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(null=False, default=False)


class Comment(models.Model):
    id_U = models.ForeignKey(Appuser, on_delete=models.CASCADE, related_name='ucomments' )
    id_D = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE, related_name='dcomments')
    score = models.PositiveIntegerField(validators=[ MinValueValidator(0), MaxValueValidator(5)])
    context = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.context[:30]}'
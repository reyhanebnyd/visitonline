from django.db import models
from django.contrib.auth.models import User
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    career = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    accessdate = models.JSONField()
    avg_visit_time = models.DecimalField(max_digits=5, decimal_places=2)


class Fulltimes(models.Model):
    id_U = models.ForeignKey(
        "user.Appuser",
        on_delete=models.CASCADE,
    )
    id_D = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
    )
    accessdate = models.DateTimeField()

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
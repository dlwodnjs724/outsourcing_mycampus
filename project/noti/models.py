from django.db import models
from accounts.models import User
from board.models import Post

# Create your models here.

class Notification(models.Model):
    _from = models.ForeignKey(User, on_delete=models.CASCADE),
    _to = models.ForeignKey(User, on_delete=models.CASCADE),
    _on = models.ForeignKey(Post, on_delete=models.CASCADE),
    _type = 
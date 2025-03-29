from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
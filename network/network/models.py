from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Follow(models.Model):
    ACTION_CHOICES = [
        ("Follow", "Follow"),
        ("Unfollow", "Unfollow"),
    ]
    
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings') # the users a user follow
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers') # the users that follow a user
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='Follow')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def is_following(user, visitor):
        if not Follow.objects.filter(following=user, followers=visitor).exists():
            return False
        return True
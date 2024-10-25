from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.CharField(max_length=64, default='Admin')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.URLField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bidder = models.CharField(max_length=64, default="None")
    category = models.CharField(max_length=64, default='Uncategorized')
    watchers = models.ManyToManyField(User, related_name='watchlist', blank=True)
    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def get_winner(self):
        if self.is_closed and self.current_bidder != 'None':
            return self.current_bidder
        return None
    
class Bid(models.Model):
    last_bid = models.DecimalField(max_digits=10, decimal_places=2)
    by_user = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.by_user} bid {self.last_bid}'
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'comment by {self.user.username} on {self.listing.title}'
    
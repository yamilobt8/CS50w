from django.contrib import admin
from .models import User, Listing, Bid, Comment

# adding database tables to admin panel
admin.site.register([User, Listing, Bid, Comment])


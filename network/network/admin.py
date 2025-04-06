from django.contrib import admin
from .models import User, Post, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
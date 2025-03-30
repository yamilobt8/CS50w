import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        'posts':posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
@csrf_exempt
def new_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Post request required'}, status=400)
    
    try:
        data = json.loads(request.body)  
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    content = data.get('content', '').strip()

    post = Post(user=request.user,content=content)
    post.save()
    
    return JsonResponse({'message': 'post posted succesully.'}, status=201)

def profile_view(request, user):
    user = get_object_or_404(User, username=user)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    
    return render(request, 'network/profile.html', {
        'user': user,
        'posts': posts
    })
    
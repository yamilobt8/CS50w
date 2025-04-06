import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


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
    is_following = Follow.is_following(user, request.user)
    followers = user.followers.count()
    followings = user.followings.count()
    
    
    return render(request, 'network/profile.html', {
        'user_profile': user,
        'posts': posts,
        'is_following': is_following,
        'followers': followers,
        'followings': followings
    })

@login_required
@csrf_exempt
def toggle_follow(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)
    
    try:
        data = json.loads(request.body)  
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    follower = get_object_or_404(User, username=data.get('follower'))
    followed = get_object_or_404(User, username=data.get('followed'))
    action = data.get('action')
    
    if not follower or not followed or not action:
        return JsonResponse({'error': 'Missng data'}, status=400)
    
    if action == 'Follow':
        Follow.objects.create(following=followed, followers=follower, action='Follow')
        return JsonResponse({'message': f'{follower} is now following {followed}.'}, status=201)
    elif action == 'Unfollow':
        Follow.objects.filter(following=followed, followers=follower).delete()
        return JsonResponse({'message': f'{follower} has unfollowed {followed}.'}, status=200)
    
    return JsonResponse({'error:': 'Invalid Action'}, status=400)


def follow_stats(request, user):
    user = get_object_or_404(User, username=user)
    followers = user.followers.count()
    followings = user.followings.count()
    
    return JsonResponse({
        'followers': followers,
        'followings': followings
    })
    
def followed_posts(request):
    user = request.user
    
    # get the followings of a user
    followings = Follow.objects.filter(followers=user, action='Follow').values_list('following', flat=True)
    posts = Post.objects.filter(user__in = followings) # get the posts of the user followings
    
    return render(request, 'network/followed.html', {
        'posts': posts
    })
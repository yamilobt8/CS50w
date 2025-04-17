import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


from .models import User, Post, Follow, Likes


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    if request.user.is_authenticated:
        liked_post_ids = Likes.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_post_ids = []
    
    p = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    total_pages = p.page_range
    
    return render(request, "network/index.html", {
        'posts':page_obj,
        'liked_posts_ids': liked_post_ids,
        'page_obj': page_obj,
        'total_pages': total_pages
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
    followers = user.followers.count()
    followings = user.followings.count()
    if request.user.is_authenticated:
        liked_post_ids = Likes.objects.filter(user=request.user).values_list('post_id', flat=True)
        is_following = Follow.is_following(user, request.user)
    else:
        liked_post_ids = []
        is_following = False
    p = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    total_pages = p.page_range
    
    return render(request, 'network/profile.html', {
        'user_profile': user,
        'posts': page_obj,
        'is_following': is_following,
        'followers': followers,
        'followings': followings,
        'liked_posts_ids': liked_post_ids,
        'page_obj': page_obj,
        'total_pages': total_pages
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
    
    # revoke user from following himself
    if follower == followed:
        return JsonResponse({'error': "User can't follow himself"}, status=403)
    
    action = data.get('action')
    
    if not follower or not followed or not action:
        return JsonResponse({'error': 'Missng data'}, status=400)
    
    if action == 'Follow' and not Follow.is_following(followed, follower):
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
    liked_post_ids = Likes.objects.filter(user=request.user).values_list('post_id', flat=True)
    p = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    total_pages = p.page_range
    return render(request, 'network/followed.html', {
        'posts': page_obj,
        'page_obj':page_obj,
        'liked_posts_ids': liked_post_ids,
        'total_pages':total_pages
    })
    
    
@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Post request required'}, status=400)
    
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        raise PermissionDenied
    
    try:
        data = json.loads(request.body)  
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    newcontent = data.get('content', '').strip()   
    post.content = newcontent
    post.been_edited = True
    post.save()
    
    return JsonResponse({'message': 'Post Updated succesfully'})


@login_required
@csrf_exempt
def like_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Post request required'}, status=400)
    
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user == post.user:
        return JsonResponse({'error': "You can't like your own post"}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    action = data.get('action')
    
    if action == 'like' and not Likes.objects.filter(user=user, post=post).exists():
        post.likes += 1
        Likes.objects.create(user=user, post=post)
    elif action == 'unlike' and post.likes > 0:
        post.likes -= 1
        Likes.objects.filter(user=user, post=post).delete()
    post.save()
    
    return JsonResponse({'message': f'Post {action}d succesfully'})

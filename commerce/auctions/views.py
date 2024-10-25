from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_listing(request):
    if request.method == 'POST':
        # deleting white spaces if there is any
        image_link = request.POST.get('link').strip()
        if not image_link:
            # setting a placeholder if the user entres nothing
            image_link = 'https://via.placeholder.com/150'
        starting_price = request.POST['price']
        listing = Listing.objects.create(
            owner = request.user.username,
            title = request.POST['title'],
            description = request.POST['description'],
            image = image_link,
            starting_bid = starting_price, # fixed starting bid
            bid = starting_price, # Initialize the current bid with the starting bid
            category = request.POST['category']
        )
        return redirect('index')

    return render(request, 'auctions/add_listing.html')

def categories(request):
    return render(request, 'auctions/categories.html')

def listing_detail(request, listing_id):
    # Getting the listing by its id if its not returning an 404 error
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the user is the owner of the listing
    is_owner = listing.owner == request.user.username

    # Check if the auction is closed and if the current user is the winner
    winner = None
    if listing.is_closed:
        winner = listing.get_winner()

    if request.method == 'POST':

        if 'bid' in request.POST:
            # Handle the bid logic
            last_bid = float(request.POST.get('bid'))
            by_user = request.user.username

            # Check if bid is higher than the current bid
            if last_bid <= listing.bid:
                return render(request, 'auctions/listing_details', {
                    'listing':listing,
                    'error': 1
                })
            
            # Prevent owner from bidding on their own listing
            if by_user == listing.owner:
                return render(request, 'auctions/listing_details', {
                    'listing': listing,
                    'error': 2
                })
            
            bid_data = Bid(last_bid=last_bid, by_user=by_user)
            bid_data.save()

            # Update the current bid and bidder
            listing.bid = last_bid
            listing.current_bidder = by_user
            listing.save()
    
            # Redirect back to the same listing page after bid
            return redirect('listing_detail', listing_id=listing.id)
        
        elif 'comment' in request.POST:
            # Handle the comment logic
            comment = request.POST.get('comment')
            if comment:
                comment = Comment(
                listing=listing,
                user=request.user,
                content=comment  # Use the 'content' field in the Comment model
            )
            comment.save()

        elif 'close_auction' in request.POST:
            if is_owner:
                listing.is_closed = True
                listing.save()
            return redirect('listing_detail', listing_id=listing.id)

        return redirect('listing_detail', listing_id=listing.id)

        
    # importing the comments for a specific listing
    comments = Comment.objects.filter(listing=listing)
    # rendering the detail page

    return render(request, 'auctions/listing_details', {
        'listing': listing,
        'comments': comments,
        'is_owner': is_owner,
        'winner': winner,
    })

@login_required
def toogle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.user in listing.watchers.all():
        #Remove from watchlist
        listing.watchers.remove(request.user)
    
    else:
        #add to watchlist
        listing.watchers.add(request.user)

    return redirect('listing_detail', listing_id=listing.id)

@login_required
def display_watchlist(request):
    #Get the listings that the user watch
    watchlist_items = request.user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        'watchlist_items': watchlist_items,
    })

def category_listings(request, category_name):
    # Get all listing in the specified category
    listings = Listing.objects.filter(category = category_name)

    return render(request, 'auctions/category_listings.html', {
        'category_name': category_name,
        'listings': listings,
    })
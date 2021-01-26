from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404

from .models import User, Listing
from .forms import ListingForm

def index(request):
    print (Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=False) # query for only active listings
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

@login_required
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
def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid(): # check if listing exists?
            data = form.cleaned_data
            listing = Listing.create(
                title=data['title'],
                description=data['description'],
                startingBid=data['startingBid'],
                imageURL=data['imageURL'],
                category=data['category'],
                userID=User.objects.get(pk=request.user.id)
            )
            listing.save()
            return HttpResponseRedirect(reverse("index")) # todo: render newly created listing
        else: # need validation error handling
            raise Http404
    else:
        form = ListingForm()
        return render(request, "auctions/createListing.html", {
            "form": form
        })

# update listing

def viewListing(request, listing_id):
    # check if listing is active or inactive
    # check if listing exists
    # if user authenticated, pass user_id from request
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })
    # can only view inactive listings if logged in

@login_required
def watchList(request):
    print (Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=False) # query for only active listings
    })

def categories(request):
    print (Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=False) # query for only active listings
    })

    # https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/ render template with local timezone

    # editListing, need login_required

# create viewUser
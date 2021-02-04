from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm

# Views allowing anonymous users

def index(request):
    #print (Listing.objects.all())
    # add error and errormessage
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all() # query for only active listings
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

# Views requiring a logged-in user

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid(): # check if listing exists? all listings are unique by pk. other fields to set unique by?
            data = form.cleaned_data
            listing = Listing.create(
                title=data['title'],
                description=data['description'],
                startingBid=data['startingBid'],
                currentBid=data['startingBid'], # currentBid starts at startingBid; foreign key to bids table?
                imageURL=data['imageURL'],
                category=data['category'],
                userID=User.objects.get(pk=request.user.id)
            )
            listing.save()
            return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))
        else: # need validation error handling
            raise Http404
    else:
        form = ListingForm()
        return render(request, "auctions/createListing.html", {
            "form": form
        })

@login_required
def updateListing(request, listingID):
    listing = Listing.objects.get(pk=listingID)
    if request.user.id == listing.owner.id and listing.active:
        if request.method == "POST":
            form = ListingForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                listing.title = data['title']
                listing.description=data['description']
                listing.startingBid=data['startingBid']
                listing.imageURL=data['imageURL']
                listing.category=data['category']
                listing.active=data['active']
                listing.save()
                return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))
            else: # need validation error handling
                raise Http404
        else: # GET request
            form = ListingForm(model_to_dict(listing)) # populate form with existing values of listing
            return render(request, "auctions/updateListing.html", {
                "listing": listing,
                "form": form
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Not able to update this listing"
        })

@login_required
def viewListing(request, listingID):
    try: # Check if listing exists
        listing = Listing.objects.get(pk=listingID)
        context = {"listing":listing}
    except:
        return HttpResponseRedirect(reverse("index"))
    context["bids"] = listing.bids_on_listing.all()
    context["comments"] = listing.comments_on_listing.all()
    context["commentForm"] = CommentForm()
    if listing.active:
        if listing.owner.id == request.user.id:
            context["owner"] = True
        else:
            context["bidForm"] = BidForm()
            try: # Check if listing on user's watchlist
                if request.user.watchList.get(pk=listingID):
                    context["on_watchList"] = True
            except ObjectDoesNotExist:
                pass
    else: # Listing not active
        context["message"] = getWinner(listing)
    return render(request, "auctions/listing.html", context)

def getWinner(listing):
    try:
        return f'Winning user is {listing.bids_on_listing.last().user}'
    except:
        return "No bids were made on this listing"

@login_required
def closeListing(request, listingID):
    try:
        listing = Listing.objects.get(pk=listingID)
    except:
        return HttpResponseRedirect(reverse("index"))
    if request.user == listing.owner:
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("viewListing", args=[listingID]))

@login_required
def submitBid(request, listingID):
    # how do client-side validation to check bidAmount is higher than listing.currentBid
    listing = Listing.objects.get(pk=listingID)
    bidForm = BidForm(request.POST)

    if bidForm.is_valid():
        amount = bidForm.cleaned_data['amount']
        if amount > listing.currentBid:
            bid = Bid.create(
                listing = listing,
                user = User.objects.get(pk=request.user.id),
                amount = bidForm.cleaned_data['amount'])
            bid.save()
            listing.currentBid = bid.amount
            listing.save()
            return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))

    # Invalid bid
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "on_watchList": True if request.user.watchList.filter(pk=listingID).count() > 0 else False,
        "bids": listing.bids_on_listing.all(),
        "bidForm": bidForm,
        "message": "Invalid bid"
    })

@login_required
def add_watchList(request, listingID):
    # Add a listing to a User's watchlist; assumes user is not owner of listing
    listing = Listing.objects.get(pk=listingID)
    request.user.watchList.add(listing)
    request.user.save()
    return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))

@login_required
def remove_watchList(request, listingID):
    # Remove a listing from a User's watchlist
    listing = Listing.objects.get(pk=listingID)
    request.user.watchList.remove(listing)
    request.user.save()
    return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))

@login_required
def view_watchList(request):
    # View a User's watchlist
    return render(request, "auctions/watchList.html", {
        "listings": request.user.watchList.all()
    })

@login_required
def categories(request): # treat like hashtags and allow users to add any they want? or provide preselected categories?
    return render(request, "auctions/categories.html")

@login_required
def addComment(request, listingID):
    listing = Listing.objects.get(pk=listingID)
    commentForm = CommentForm(request.POST)

    if commentForm.is_valid():
        comment = Comment.create(
            listing = listing,
            user = User.objects.get(pk=request.user.id),
            content = commentForm.cleaned_data['content'])
        comment.save()
    return HttpResponseRedirect(reverse("viewListing", args=[listing.id]))

@login_required
def deleteComment(request, listingID):
    pass

# def viewUser
    # see a user's profile
    # shows username, date joined

# def viewUserBids
    # see all bids created by the logged in user

# improve front end layout - bootstrap
# https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/ render template with local timezone
# how apply decorator to multiple views
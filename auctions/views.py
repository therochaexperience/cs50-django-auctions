from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid
from .forms import ListingForm, BidForm

# Views allowing anonymous users

def index(request):
    #print (Listing.objects.all())
    # add error and errormessage
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True) # query for only active listings
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
    if request.user.id == listing.owner.id:
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
def submitBid(request, listingID):
    # how do client-side validation to check bidAmount is higher than listing.currentBid
    
    if request.method == "GET":
        return HttpResponseRedirect(reverse("viewListing", args=[listingID]))
    else:
        try:
            listing = Listing.objects.get(pk=listingID)
        except:
            return HttpResponseRedirect(reverse("index"))
        if request.user == listing.owner.id or not listing.active:
            return HttpResponseRedirect(reverse("viewListing", args=[listingID]))

        bidForm = BidForm(request.POST)
        invalid_bid_context = {
            "listing": listing,
            "on_watchList": True if request.user.watchList.filter(pk=listingID).count() > 0 else False,
            "bids": listing.bids_on_listing.all(),
            "bidForm": bidForm,
            "message": "Invalid bid"
        }
        if bidForm.is_valid(): # create bid record
            print(listing.bids_on_listing.all())
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
            else:
                return render(request, "auctions/listing.html", invalid_bid_context)
        else: # need validation error handling
            return render(request, "auctions/listing.html", invalid_bid_context)

@login_required
def viewListing(request, listingID):
    try:
        listing = Listing.objects.get(pk=listingID)
    except:
        return HttpResponseRedirect(reverse("index"))
    if listing.active:
        bids = listing.bids_on_listing.all()
        if listing.owner.id == request.user.id:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "owner": True,
                "bids": bids
            })
        else:
            bidForm = BidForm()
            try: # DRY?
                if request.user.watchList.get(pk=listingID):
                    return render(request, "auctions/listing.html", {
                        "on_watchList": True,
                        "listing": listing,
                        "bidForm": bidForm,
                        "bids": bids
                    })
            except ObjectDoesNotExist:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bidForm": bidForm,
                    "bids": bids
                })
    else: # Listing not active
        # add redirect to index with error message stating that listing is no longer active
        # can only view inactive listings if logged in and owner
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "This listing is no longer active"
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
def categories(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=False) # query for only active listings
    })



# close a listing
    # closing a listing means listings are no longer active

# create viewUser


# add link for Your Bids

# https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/ render template with local timezone
# how apply decorator to multiple views
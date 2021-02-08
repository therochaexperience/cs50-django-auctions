from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("categories", views.categories, name="categories"),
    path("createListing", views.createListing, name="createListing"),
    path("viewListing/<int:listingID>", views.viewListing, name="viewListing"),
    path("updateListing/<int:listingID>", views.updateListing, name="updateListing"),
    path("closeListing/<int:listingID>", views.closeListing, name="closeListing"),
    path("view_watchList", views.view_watchList, name="view_watchList"), # View a user's watchlist; user needs to be authenticated
    path("add_watchList/<int:listingID>", views.add_watchList, name="add_watchList"),
    path("remove_watchList/<int:listingID>", views.remove_watchList, name="remove_watchList"),
    path("submitBid/<int:listingID>", views.submitBid, name="submitBid"),
    path("viewUserBids", views.viewUserBids, name="viewUserBids"),
    path("addComment/<int:listingID>", views.addComment, name="addComment"),
    path("deleteComment/<int:listingID>", views.deleteComment, name="deleteComment")
]

# Overloading createListing method. If called with no parameter, render page.
# If called with a parameter (listing object), then create listing.

# how to remember original path of user? if unauthenticated user goes to
# createListing page, then logs in, after logging in, the user should be
# redirected back to the createListing page to continue creating a listing.
# minimize friction to creating listings and generating profits.

# how to uniquely identify a listing
# how to get username of user that created a listing

# can unique messages be passed to layout.html from createListing or other views?

# on createListing path, if user is authenticated, go to createListing, else redirect to ""

# autoformating currency field in createListing
# https://codepen.io/559wade/pen/LRzEjj

# validate starting bid is entered correctly

# place enter amount label inline with starting bid text box

# need to validate URLs for images
# need to validate categories
# how to filter for NSFW images or categories
# https://docs.djangoproject.com/en/3.1/ref/validators/

# authentication
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#the-login-required-decorator

# how to bulk load a csv file

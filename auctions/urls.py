from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("watchList", views.watchList, name="watchList"),
    path("categories", views.categories, name="categories"),
    path("viewListing/<int:listingID>", views.viewListing, name="viewListing"),
    path("updateListing/<int:listingID>", views.updateListing, name="updateListing")
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

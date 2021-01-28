from django.forms import ModelForm
from django import forms
from .models import Listing

class ListingForm(ModelForm): # how to create initial values
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingBid', 'imageURL', 'category', 'active']
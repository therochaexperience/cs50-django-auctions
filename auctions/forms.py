from django.forms import ModelForm
from django import forms
from .models import Listing, Bid, Comment

class ListingForm(ModelForm): # how to create initial values
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingBid', 'imageURL', 'category', 'active']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            "amount": "Bid Amount"
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            "content": "Add Comment"
        }
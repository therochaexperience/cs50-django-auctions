from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    startingBid = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]) # not validating for min bid
    # currentBid?
    imageURL = models.URLField()
    category = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    #dateTimeEndListing = models.DateTimeField() # change to durationfield?; add to createListing form
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listingOwner",
        default='0')

    def __str__(self):
        return f"Listing {self.id}: {self.title} by User: {self.owner}"

    @classmethod # DRY?
    def create(cls, title, description, startingBid, imageURL, category, userID):
        listing = cls(
            title=title,
            description=description,
            startingBid=startingBid,
            imageURL=imageURL,
            category=category,
            owner=userID)
        return listing

    # add method to update listing end datetime
    # a list of bids
    # a list of comments

# bids
    # which listing
    # which user
    # what amount
    # date

# comments
    # which listing
    # which user
    # comment contents
    # date
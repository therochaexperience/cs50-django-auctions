from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class User(AbstractUser):
    watchList = models.ManyToManyField('Listing')

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    startingBid = models.DecimalField(
        default=0.01,
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))] # not validating for min bid
    )
    currentBid = models.DecimalField( # who has done current bid, which is largest?
        default=0.01,
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    imageURL = models.URLField()

    CategoryType = models.TextChoices('CategoryType', 
    'Books Computers Electronics Events Food Games Home Outdoors RANDOM')
    category = models.CharField(max_length=25, choices=CategoryType.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    #dateTimeEndListing = models.DateTimeField() # change to durationfield?; add to createListing form
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings_created",
        default='0')

    def __str__(self):
        return f"Listing {self.id}: {self.title} by User: {self.owner}"

    @classmethod # DRY?
    def create(cls, title, description, startingBid, currentBid, imageURL, category, userID, active):
        listing = cls(
            title=title,
            description=description,
            startingBid=startingBid,
            currentBid=currentBid,
            imageURL=imageURL,
            category=category,
            owner=userID,
            active=active)
        return listing

class Bid(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids_on_listing"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids_by_user"
    )
    amount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
   
    @classmethod # DRY?
    def create(cls, listing, user, amount):
        bid = cls(
            listing = listing,
            user = user,
            amount = amount)
        return bid

    def __str__(self):
        return f"Bid {self.id} on Listing {self.listing.title} by User: {self.user}"

class Comment(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments_on_listing"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments_by_user"
    )
    content = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
   
    @classmethod # DRY?
    def create(cls, listing, user, content):
        comment = cls(
            listing = listing,
            user = user,
            content = content)
        return comment
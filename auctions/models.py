from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class User(AbstractUser):
    watchList = models.ManyToManyField('Listing')

class Category(models.Model):
    name = models.CharField(max_length=25, primary_key=True) #, unique=True
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod # DRY?
    def create(cls, name):
        category = cls(name = name)
        return category

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
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="listings",
        default='0'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    #dateTimeEndListing = models.DateTimeField() # change to durationfield?; add to createListing form
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings_created",
        default='0')

    def __str__(self):
        return f"Listing {self.id}: {self.title} by User: {self.owner}"

    @classmethod # DRY?
    def create(cls, title, description, startingBid, currentBid, imageURL, category, userID):
        listing = cls(
            title=title,
            description=description,
            startingBid=startingBid,
            currentBid=currentBid,
            imageURL=imageURL,
            category=category,
            owner=userID)
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
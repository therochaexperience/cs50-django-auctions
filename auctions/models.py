from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    startingBid = models.IntegerField()
    imageURL = models.URLField()
    category = models.CharField(max_length=25)
    dateTimeCreated = models.DateTimeField(auto_now_add=True)
    #dateTimeEndListing = models.DateTimeField() # change to durationfield?; add to createListing form
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listingOwner")

    def __str__(self):
        return f"Listing {self.id}: {self.title}" # by User: {self.owner}"

    # create method
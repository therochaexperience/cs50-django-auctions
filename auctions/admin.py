from django.contrib import admin
from .models import Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "dateTimeCreated")

admin.site.register(Listing)

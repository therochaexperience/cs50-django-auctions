from django.contrib import admin
from .models import Listing, Bid, Comment

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created_at")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "created_at")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at",  "content")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)


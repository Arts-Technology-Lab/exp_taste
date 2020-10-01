from django.contrib import admin
from main.models import Auction, AuctionLot, Artwork, ArtImage, Artist

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "city")
    list_filter=("start_date",)
    search_fields = ("title",)
    

@admin.register(AuctionLot)
class AuctionLotAdmin(admin.ModelAdmin):
    pass

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    pass

@admin.register(ArtImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from main.models import Auction, AuctionLot, Artwork, ArtImage, Artist

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "city")
    list_filter=("start_date", "collected")
    search_fields = ("title",)


def lot_auction_title(obj):
    return obj.auction.title
lot_auction_title.short_description = "Auction Title"

@admin.register(AuctionLot)
class AuctionLotAdmin(admin.ModelAdmin):
    search_fields = ("auction__title",)
    list_display = (lot_auction_title, "lot_number")
    list_display_links = (lot_auction_title, "lot_number")

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    pass

@admin.register(ArtImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from main.models import (Auction, AuctionLot, Artwork, ArtImage, Artist, 
                         LotImage, Category, AboutPage)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "end_date", "category")
    list_filter=("end_date", "collected", "category")
    search_fields = ("title",)
    list_editable = ("category",)

class LotImageInline(admin.TabularInline):
    model = LotImage

def lot_auction_title(obj):
    return obj.auction.title
lot_auction_title.short_description = "Auction Title"

@admin.register(AuctionLot)
class AuctionLotAdmin(admin.ModelAdmin):
    search_fields = ("auction__title", "title", "id")
    list_display = (lot_auction_title, "lot_number", "title")
    list_display_links = (lot_auction_title, "lot_number", "title")
    list_filter = ("visited", "collected")
    inlines = [LotImageInline]

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    pass

@admin.register(ArtImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)
    readonly_fields = ("name_slug", )
    
@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('truncate_text', 'current')
    list_editable =  ('current',)

    def truncate_text(self, obj):
        return obj.text[:20]
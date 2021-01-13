from django.db import models

class Auction(models.Model):
    title = models.CharField("Title", max_length=255)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    collected = models.BooleanField("Artworks collected", default=False)
    url = models.URLField("URL", unique=True, max_length=2000)
    city = models.CharField("City", max_length=200, default="")

    class Meta:
        db_table = "auctions"
        ordering = ["-end_date", "id"]

    def __str__(self):
        return self.title[:20]


class AuctionLot(models.Model):
    lot_number = models.IntegerField("Lot Number")
    artwork = models.ForeignKey("Artwork",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    auction = models.ForeignKey("Auction",
                                on_delete=models.CASCADE)
    estimate_low = models.IntegerField("Estimate Low Value",
                                       null=True,
                                       blank=True)
    estimate_high = models.IntegerField("Estimate High Value",
                                        null=True,
                                        blank=True)
    estimate_currency = models.CharField("Estimate Currency",
                                         max_length=3,
                                         default="USD")
    sale_price = models.IntegerField("Sale Price",
                                     null=True,
                                     blank=True)
    sale_currency = models.CharField("Sale Currency",
                                     max_length=3,
                                     default="USD")
    number_of_bids = models.IntegerField("Number of Bids",
                                         default=1)
    reserve_met = models.BooleanField("Reserve Met",
                                      default=True)
    condition_report = models.TextField("Condition Report",
                                        default="")
    provenance = models.TextField("Provenance",
                                  default="")
    url = models.URLField("URL", max_length=2000, default="")
    visited = models.BooleanField("Visited", default=False)

    class Meta:
        db_table = "auction_lots"
        verbose_name = "Auction Lot"
        verbose_name_plural = "Auction Lots"
        ordering = ["auction__id", "lot_number"]

    def __str__(self):
        return f"Lot {self.lot_number} - {self.auction}"

    
class Artwork(models.Model):
    title = models.CharField("Title", max_length=255)
    artist = models.ForeignKey("Artist",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    
    executed = models.IntegerField("Year Executed")
    medium = models.CharField("Medium",
                              max_length=255)
    dimensions = models.CharField("Dimensions",
                                  max_length=255)
    
    
    class Meta:
        verbose_name = "Art Work"
        verbose_name_plural = "Art Works"
        db_table = "artworks"


class ArtImage(models.Model):
    image = models.ImageField()
    artwork = models.ForeignKey("Artwork",
                                on_delete=models.CASCADE)
    featured = models.BooleanField("Featured Photo", default=False)



    class Meta:
        verbose_name = "Art Image"
        verbose_name_plural = "Art Images"
        db_table = "art_images"

    def __str__(self):
        return self.image.file.name
    

class Artist(models.Model):
    name = models.CharField("Name", max_length=255)
    birth_year = models.IntegerField("Born",
                                     null=True,
                                     blank=True)
    death_year = models.IntegerField("Died",
                                     null=True,
                                     blank=True)

    class Meta:
        db_table = "artists"

    def __str__(self):
        return self.name[:30]
        

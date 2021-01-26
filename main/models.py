from django.db import models
from django.utils.text import slugify
# $1 USD in other currencies
TO_USD = {
    "EUR": 0.82,
    "SGD": 1.33,
    "AUD": 1.3,
    "USD": 1.0,
    "RMB": 6.48,
    "INR": 73.0,
    "GBP": 0.73,
    "CHF": 0.89,
    "HKD": 7.75,
    "CAD": 1.27
}

CURRENCY_SYMBOLS = {
    "EUR": "€",
    "SGD": "S$",
    "AUD": "$",
    "USD": "$",
    "RMB": "CN¥",
    "INR": "₨",
    "GBP": "£",
    "CHF": "Fr",
    "HKD": "$",
    "CAD": "$"
}



def convert_usd(amount, currency):
    res = amount / TO_USD.get(currency)
    return int(res)

class Auction(models.Model):
    title = models.CharField("Title", max_length=255)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    collected = models.BooleanField("Artworks collected", default=False)
    attempted = models.BooleanField("Collection attempted", default=False)
    url = models.URLField("URL", unique=True, max_length=2000)
    city = models.CharField("City", max_length=200, default="")

    class Meta:
        db_table = "auctions"
        ordering = ["-end_date", "id"]

    def __str__(self):
        return self.title[:20]


class AuctionLot(models.Model):
    lot_number = models.CharField("Lot Number", 
                                  default="",
                                  max_length=20)
    title = models.CharField("Title", 
                             max_length=1000, 
                             default="")                                  
    description = models.TextField("Description",
                                   default="")                             
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
    sale_price_usd = models.IntegerField("Sale Price in USD",
                                         null=True,
                                         blank=True) 
    number_of_bids = models.IntegerField("Number of Bids",
                                         default=1)
    reserve_met = models.BooleanField("Reserve Met",
                                      default=False)
    condition_report = models.TextField("Condition Report",
                                        default="",
                                        blank=True)
    provenance = models.TextField("Provenance",
                                  default="", 
                                  blank=True)
    url = models.URLField("URL", max_length=2000, default="")
    visited = models.BooleanField("Visited", default=False)
    collected = models.BooleanField("Collected", default=False)

    @property
    def currency_symbol(self):
        currency = self.sale_currency or self.estimate_currency
        return CURRENCY_SYMBOLS.get(currency, "$")

    class Meta:
        db_table = "auction_lots"
        verbose_name = "Auction Lot"
        verbose_name_plural = "Auction Lots"
        ordering = ["auction__id", "lot_number"]

    def __str__(self):
        return f"Lot {self.lot_number} - {self.auction}"

    def save(self, *args, **kwargs):
        if self.sale_currency in TO_USD:
            self.sale_price_usd = convert_usd(self.sale_price, 
                                              self.sale_currency)
        return super().save(*args, **kwargs)

    
class Artwork(models.Model):
    title = models.CharField("Title", max_length=255)
    title_slug = models.SlugField("Title Slug", 
                                  max_length=255, 
                                  editable=False,
                                  default="")
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        return super().save(*args, **kwargs)


def lot_image_path(instance, filename):
    return (f"auctions/{instance.lot.auction.id}/"
            f"lots/{instance.lot.id}/{filename}")

class LotImage(models.Model):
    image = models.ImageField(upload_to=lot_image_path)
    lot = models.ForeignKey("AuctionLot",
                            on_delete=models.CASCADE)
    source = models.URLField("Source URL", default="")

    class Meta:
        verbose_name = "Lot Image"
        verbose_name_plural = "Lot Images"
        db_table = "lot_images"
    
    def __str__(self):
        return self.image.file.name


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
    name_slug = models.SlugField("Name Slug", 
                                 max_length=255, 
                                 editable=False,
                                 default="")
    birth_year = models.IntegerField("Born",
                                     null=True,
                                     blank=True)
    death_year = models.IntegerField("Died",
                                     null=True,
                                     blank=True)

    class Meta:
        db_table = "artists"

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name[:30]
        

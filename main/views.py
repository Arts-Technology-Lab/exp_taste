import random

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import AuctionLot, LotImage

class Home(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = random.choice(AuctionLot
                          .objects
                          .filter(collected=True, sale_price__isnull=False))
                          
        min_year = a.auction.end_date.year - 1
        max_year = a.auction.end_date.year + 1
        b = random.choice(AuctionLot
                          .objects
                          .filter(collected=True, sale_price__isnull=False,
                                 auction__end_date__year__gte=min_year,
                                 auction__end_date__year__lte=max_year)
                          .exclude(id=a.id))
        context["lot_a"] = a
        context["lot_a_img"] = a.lotimage_set.all()[0]
        context["lot_b"] = b
        context["lot_b_img"] = b.lotimage_set.all()[0]

        return context

import random
import datetime

from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import AboutPage, AuctionLot, Auction

START_KEY = "oldest_auction"
END_KEY = "newest_auction"
three_years = datetime.timedelta(days=365.25 * 3)
one_year = datetime.timedelta(days=365.25)


class Home(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        # To select two random auction lots to compare:
        # 1. Only consider lots where collected is true and a sale price is set
        # 2. Random select a date between the oldest and newest valid lots
        # 3. Randomly select valid lots between one year before and one year after the selected date
        # the oldest and newest dates won't change that often unless we scrape more data
        # so cache them to avoid hitting the database every time
        context = super().get_context_data(**kwargs)
        oldest_auction = cache.get(START_KEY)
        if not oldest_auction:
            oldest_auction = (
                AuctionLot.objects.filter(collected=True, sale_price__isnull=False)
                .order_by("auction__end_date")
                .values("auction__end_date")[0]["auction__end_date"]
            )
            cache.set(START_KEY, oldest_auction, timeout=None)

        newest_auction = cache.get(END_KEY)

        if not newest_auction:
            newest_auction = (
                AuctionLot.objects.filter(collected=True, sale_price__isnull=False)
                .order_by("-auction__end_date")
                .values("auction__end_date")[0]["auction__end_date"]
            )
            cache.set(END_KEY, newest_auction, timeout=None)

        duration = (newest_auction - oldest_auction).total_seconds()

        random_date = oldest_auction + datetime.timedelta(
            seconds=random.randint(86400, duration)
        )
        period_start = max(oldest_auction, random_date - one_year)
        period_end = min(newest_auction, random_date + one_year)
        candidates = AuctionLot.objects.filter(
            collected=True,
            sale_price__isnull=False,
            auction__end_date__gte=period_start,
            auction__end_date__lte=period_end,
        )
        num_candidates = candidates.count()
        if num_candidates > 2:
            selected = random.sample(range(0, num_candidates), 2)
            a = candidates[selected[0]]
            b = candidates[selected[1]]
            context["lot_a"] = a
            context["lot_a_img"] = a.lotimage_set.all()[0]
            context["lot_b"] = b
            context["lot_b_img"] = b.lotimage_set.all()[0]

        return context


def about(request):
    try:
        page = AboutPage.objects.filter(current=True)[0]
    except IndexError:
        return render(request, "pages/about.html")

    return render(request, "main/about.html", context={"copy": page.html})

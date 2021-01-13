import datetime
import re
import time

import requests
from django.db import IntegrityError
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver import Firefox

from main.models import (Auction, AuctionLot, Artwork, ArtImage, Artist)

dstrs = ["22 September 2020",
         "21–30 September 2020",
         "28 August–9 September 2020",
         "23 November 2018–25 January 2019"]

DEPARTMENTS = [
    ("Contemporary Art", "00000164-609b-d1db-a5e6-e9ff01230000"),
    ("Impressionist & Modern Art", "00000164-609b-d1db-a5e6-e9ff08ab0000"),
    ("Chinese Works of Art", "00000164-609b-d1db-a5e6-e9ff0b150000"),
    ("19th Century European Paintings", "00000164-609a-d1db-a5e6-e9fff79f0000"),
    ("19th Century Furniture & Sculpture", "00000164-609b-d1db-a5e6-e9ff043c0000"),
    ("20th Century Design", "00000164-609a-d1db-a5e6-e9fffe5f0000"),
    ("Aboriginal Art", "00000164-609a-d1db-a5e6-e9ffff8d0000"),
    ("African & Oceanic Art", "00000164-609b-d1db-a5e6-e9ff01850000"),
    ("African Modern & Contemporary Art", "00000164-609a-d1db-a5e6-e9fffdf80000"),
    ("American Art", "00000164-609b-d1db-a5e6-e9ff0a800000"),
    ("Ancient Sculpture and Works of Art", "00000164-609a-d1db-a5e6-e9fff35f0000"),
    # ("Automobiles | RM Sotheby's", "00000164-609a-d1db-a5e6-e9fffd920000"),
    # ("Books & Manuscripts", "00000164-609b-d1db-a5e6-e9ff03270000"),
    ("British Paintings 1550-1850", "00000164-609b-d1db-a5e6-e9ff06270000"),
    ("British Watercolours & Drawings 1550-1850", "00000164-609a-d1db-a5e6-e9fff8660000"),
    ("Canadian Art", "00000164-609a-d1db-a5e6-e9fffffb0000"),
    ("Chinese Paintings – Classical", "00000164-609b-d1db-a5e6-e9ff08440000"),
    ("Chinese Paintings – Modern", "00000164-609b-d1db-a5e6-e9ff0ba60000"),
    # ("Clocks & Barometers", "00000164-609b-d1db-a5e6-e9ff00600000"),
    # ("Coins and Medals", "00000164-609b-d1db-a5e6-e9ff0c320000"),
    ("Contemporary Arab, Iranian & Turkish Art", "00000164-609a-d1db-a5e6-e9fffd2c0000"),
    ("Contemporary Ink Art", "00000164-609a-d1db-a5e6-e9fff6760000"),
    ("English Furniture", "00000164-609b-d1db-a5e6-e9ff0b610000"),
    ("European Ceramics", "00000164-609a-d1db-a5e6-e9fff9320000"),
    ("European Sculpture & Works of Art", "00000164-609a-d1db-a5e6-e9fffa760000"),
    ("French & Continental Furniture", "00000164-609b-d1db-a5e6-e9ff0bec0000"),
    # ("Handbags and Accessories", "0000016d-01ed-d6c8-a77d-19ff8f010001"),
    # ("House Sales & Private Collections", "00000164-609a-d1db-a5e6-e9fffa0b0000"),
    ("Indian, Himalayan & Southeast Asian Art", "00000164-609a-d1db-a5e6-e9ffff270000"),
    ("Indian & South Asian Modern & Contemporary Art", "00000164-609b-d1db-a5e6-e9ff07220000"),
    ("Irish Art", "00000164-609b-d1db-a5e6-e9ff068c0000"),
    ("Islamic Art", "00000164-609b-d1db-a5e6-e9ff09100000"),
    ("Israeli & International Art", "00000164-609b-d1db-a5e6-e9ff055d0000"),
    ("Japanese Art", "00000164-f0d1-d221-a575-f2fda8e90000"),
    ("Judaica", "00000164-609a-d1db-a5e6-e9fffb460000"),
    ("Latin American Art", "00000164-609b-d1db-a5e6-e9ff0a350000"),
    # (" Luxury Collectibles", "0000016d-16fd-d23f-affd-f6fdebac0001"),
    ("Modern & Contemporary Southeast Asian Art", "00000164-609b-d1db-a5e6-e9ff04fc0000"),
    ("Modern & Post-War British Art", "00000164-609b-d1db-a5e6-e9ff02b50000"),
    ("Modern Asian Art", "00000164-609a-d1db-a5e6-e9fff8ca0000"),
    # ("Musical Instruments", "00000164-609a-d1db-a5e6-e9fffc6a0000"),
    ("Objects of Vertu", "00000164-609a-d1db-a5e6-e9fff4f10000"),
    ("Old Master Drawings", "00000164-609b-d1db-a5e6-e9ff07e20000"),
    ("Old Master Paintings", "00000164-609a-d1db-a5e6-e9fffadc0000"),
    ("Orientalist Paintings", "00000164-609a-d1db-a5e6-e9fff5b50000"),
    ("Photographs", "00000164-609a-d1db-a5e6-e9fff73c0000"),
    ("Pre-Columbian Art", "00000164-609b-d1db-a5e6-e9ff03900000"),
    ("Prints", "00000164-609b-d1db-a5e6-e9ff09a60000"),
    # ("Rugs & Carpets", "00000164-609b-d1db-a5e6-e9ff09ed0000"),
    ("Russian Art", "00000164-609a-d1db-a5e6-e9fffec40000"),
    ("Scottish Art", "00000164-609a-d1db-a5e6-e9fff3c20000"),
    # ("Silver", "00000164-609a-d1db-a5e6-e9fffba40000"),
    # ("Special Projects", "00000164-609b-d1db-a5e6-e9ff049d0000"),
    # ("Spirits", "0000016d-6f17-ddcf-a3ed-ff7fde360000"),
    # ("Stamps", "00000164-609b-d1db-a5e6-e9ff024e0000"),
    ("Swiss Art", "00000164-609b-d1db-a5e6-e9ff0acd0000"),
    ("Victorian, Pre-Raphaelite & British Impressionist Art", "00000164-609a-d1db-a5e6-e9fff6150000"),
    # ("Wine & Spirits", "00000164-609a-d1db-a5e6-e9fffcc80000"),
]

BASE_URL = "https://www.sothebys.com/en/results"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
MDASH = "–"
def build_url():
    return "?".join([BASE_URL,
                     "&".join(["from=",
                               "to="] + [f"f2={d[1]}" for d in DEPARTMENTS])])

def parse_date(dstr):
    sp = dstr.split(MDASH)
    if len(sp) == 1:
        # only one date
        start_date = parse(sp[0])
        end_date = start_date
        
    elif sp[0].isdigit():
        # two days, same month and year
        start_day = int(sp[0])
        end_date = parse(sp[1])
        start_date = datetime.date(year=end_date.year,
                                   month=end_date.month,
                                   day=start_day)
    elif re.match(r'\d{4}$', sp[0]):
        # different day, month, and year
        start_date = parse(sp[0])
        end_date = parse(sp[1])
    else:
        # different day and month, same year
        end_date = parse(sp[1])
        start_date = parse(f"{sp[0]} {end_date.year}")
    return start_date, end_date
    
def auction_data(card):
    """Extract auction data from card div"""
    url = card.a["href"]
    title = card.find_all("div", class_="Card-title")[0].text
    details = card.find_all("div", class_="Card-details")[0].text
    dstr = details.split(" | ")[0]
    start_date, end_date = parse_date(dstr)
    city = details.split(" | ")[-1]
    return {"title": title,
            "url": url,
            "start_date": start_date,
            "end_date": end_date,
            "city": city}
    
def get_auctions():
    """Visit all auction listing pages and save auction info"""
    url = build_url()
    for page in range(1, 209):
        res = requests.get(url + f"&p={page}", headers={"User-Agent": UA})
        soup = BeautifulSoup(res.content, features="html.parser")
        cards = soup.find_all("div", class_="Card data-type-auction")
        for card in cards:
            data = auction_data(card)
            defaults={"title": data["title"],
                      "start_date": data["start_date"],
                      "end_date": data["end_date"],
                      "city": data["city"]}
            auction, created = Auction.objects.get_or_create(url=data["url"],
                                                             defaults=defaults)

            if not auction.city and not created:
                auction.city = data["city"]
                auction.save()
                print(f"updated city {auction.title}")

        time.sleep(15)
            

def scroll_to_end(driver):
    # adapted from:
    # https://stackoverflow.com/questions/63647849/scroll-to-the-end-of-the-infinite-loading-page-using-selenium-python
    # Get scroll height after first time page load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                lm = driver.find_element_by_css_selector("p.css-1oie00y")
                lm.click()
            except:
                break
        last_height = new_height

class LotParseException(Exception):
    pass

def create_lot(lot_div, auction):
    title = lot_div.find_element_by_css_selector("h3.css-1i601rm-h3-regular")
    m = re.match(r'^\d+', title.text)
    lot_number = None
    if m:
        lot_number = int(m.group())
    if not lot_number:
        raise LotParseException(f"Error parsing: {lot_div.text}")
    
    h4s = lot_div.find_elements_by_css_selector("h4.css-xnoh5a")
    low, high, currency = None, None, None
    for h4 in h4s:
        m = re.match(r'([\d,\.]+) - ([\d,\.]+) ([A-Z]{3})', h4.text)
        if m:
            low, high, currency = m.groups()
            low = int(re.sub(r'[,\.]', '', low))
            high = int(re.sub(r'[,\.]', '', high))
    try:
        # link = lot_div.find_element_by_css_selector("a.css-1um49bp")
        link = lot_div.find_element_by_css_selector("div > a")
    except:
        raise LotParseException(f"Could not find link at {lot_div.text}")
    possible_price = lot_div.find_elements_by_css_selector("span.css-8fe5tn-label-bold")
    sale_price, sale_currency = None, None
    for p in possible_price:
        m = re.match(r'([\d,\.]+) ([A-Z]{3})', p.text)
        if m:
            sale_price, sale_currency = m.groups()
            sale_price = int(re.sub(r'[,\.]', '', sale_price))

    lot = AuctionLot(lot_number=lot_number,
                     url = link.get_attribute("href"),
                     auction=auction)
    if sale_price and sale_currency:
        lot.sale_price = sale_price
        lot.sale_currency = sale_currency
    if all([low, high, currency]):
        lot.estimate_low = low
        lot.estimate_high = high
        lot.estimate_currency = currency
    return lot
        
def save_lots(auction):

    with Firefox() as driver:
        driver.get(auction.url)
        scroll_to_end(driver)
        lot_divs = driver.find_elements_by_css_selector("div.css-1up9enl")
        lots = [create_lot(div, auction) for div in lot_divs]
    AuctionLot.objects.bulk_create(lots)
    auction.collected = True
    auction.save()
        
def collect_lots():
    uncollected = Auction.objects.filter(collected=False)
    for auction in uncollected:
        save_lots(auction)
        time.sleep(15)

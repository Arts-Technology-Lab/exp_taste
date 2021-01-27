import datetime
import json
import re
import pathlib
import time

from io import BytesIO

import requests
import PIL

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver import Firefox

from main.models import (Auction, AuctionLot, LotImage)

dstrs = ["22 September 2020",
         "21–30 September 2020",
         "28 August–9 September 2020",
         "23 November 2018–25 January 2019"]
# HEADERS = {
#     "User-Agent": "Expensive Taste Crawler - admin@expensivetaste.art"
# }         

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
}

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
    """
    Parse first type of lot listing page
    """
    txt = lot_div.text.upper().split("\n")
    if not txt:
        raise LotParseException(f"No text: {lot_div.text}")
    m = re.match(r'^[A-Za-z0-9]+', txt[0])
    lot_number = None
    if m:
        lot_number = m.group()
    if not lot_number:
        raise LotParseException(f"Could not find lot number: {lot_div.text}")

    try:
        link = lot_div.find_element_by_css_selector("[href]")
    except:
        raise LotParseException(f"Could not find link at {lot_div.text}")

    lot = AuctionLot(lot_number=lot_number,
                     url = link.get_attribute("href"),
                     auction=auction)        
    
    if "ESTIMATE: " in txt:
        est = txt[txt.index("ESTIMATE: ") + 1]
        low, high, currency = None, None, None
        m = re.match(r'([\d,\.]+) - ([\d,\.]+) ([A-Z]{3})', est)
        if m:
            low, high, currency = m.groups()
            lot.estimate_low = int(re.sub(r'[,\.]', '', low))
            lot.estimate_high = int(re.sub(r'[,\.]', '', high))
            lot.estimate_currency = currency

    if "LOT SOLD: " in txt:
        sale = txt[txt.index("LOT SOLD: ") + 1]
        sale_price, sale_currency = None, None
        m = re.match(r'([\d,\.]+) ([A-Z]{3})', sale)
        if m:
            sale_price, sale_currency = m.groups()
            lot.sale_price = int(re.sub(r'[,\.]', '', sale_price))
            lot.sale_currency = sale_currency
    return lot

def create_lot2(article, auction):
    """
    Parse second type of lot listing page
    """
    lot_num = article.get_attribute("data-lot")
    lot_url = (article
               .find_elements_by_css_selector("div.details h4 a")[0]
               .get_attribute("href"))
    lot = AuctionLot(lot_number=lot_num,
                     url=lot_url,
                     auction=auction)  
    from_elem = article.find_elements_by_css_selector("[data-range-from]")
    if from_elem:
        lot.estimate_low = int(from_elem[0].get_attribute("data-range-from"))

    to_elem = article.find_elements_by_css_selector("[data-range-to]")
    if to_elem:
        lot.estimate_high = int(to_elem[0].get_attribute("data-range-to"))

    curr_elem = article.find_elements_by_css_selector("div.currency-dropdown a")
    if curr_elem:
        lot.estimate_currency = curr_elem[0].text
    
    sale_elem = article.find_elements_by_css_selector("[data-lot-sold]")
    if sale_elem:
        lot.sale_price = int(sale_elem[0].get_attribute("data-lot-sold"))
        lot.sale_currency = lot.estimate_currency
    
    return lot
        
def save_lots(auction):
    auction.attempted = True
    with Firefox() as driver:
        print(f"Getting {auction.url}")
        driver.get(auction.url)
        scroll_to_end(driver)
        lot_divs = driver.find_elements_by_css_selector("div.css-1up9enl")
        if lot_divs:
            lots = [create_lot(div, auction) for div in lot_divs]
        else:
            lot_divs = driver.find_elements_by_css_selector("article.sale-article")
            lots = [create_lot2(div, auction) for div in lot_divs]
    if len(lots) > 0:
        print(f"Saving {len(lots)} lots for {auction.title}")
        AuctionLot.objects.bulk_create(lots)
        auction.collected = True
    else:
        print("Could not find lots")
    auction.save()
        
def collect_lots():
    unattempted = Auction.objects.filter(attempted=False)
    for auction in unattempted:
        save_lots(auction)
        time.sleep(15)

def get_image_url(soup):
    try:
        url = soup.find("meta", attrs={"property": "og:image"}).attrs["content"]
    except:
        try: 
            url = soup.find("img", class_="main-image").attrs["src"]
            url = f"https://sothebys.com{url}"
        except:
            raise LotParseError("Couldn't find image url")
    return url


def save_image(soup, lot):
    url = get_image_url(soup)
    print(f"fetching image from {url}")
    lot_img = LotImage(source=url,
                       lot=lot)
    r = requests.get(url, headers=HEADERS)
    ct = r.headers.get("Content-Type", "")
    if ct != "image/jpeg":
        raise LotParseError("Unknown image type")
    cf = ContentFile(r.content)
    filename = f"{slugify(lot.title)}.jpg"
    lot_img.image = InMemoryUploadedFile(cf,
                                         None,
                                         filename,
                                         "image/jpeg",
                                         cf.tell,
                                         None)
    lot_img.save()                                         

class LotParseError(Exception):
    pass

def lot_from_json(soup):
    """
    Use the ld+json meta data to extract lot details from the page
    """
    ld_json = soup.find_all(type="application/ld+json")
    if not ld_json:
        raise LotParseError("No ld+json data on page")
    data = json.loads(ld_json[0].contents[0])
    data = data[0]
    item = data["mainEntity"]["offers"]["itemOffered"][0]
    description = item["description"]
    title = item["name"]
    condition_report = item["itemCondition"]
    return {"description": description,
            "title": title,
            "condition_report": condition_report}

    
def lot_from_meta(soup):
    d_meta = (soup
              .find("meta", 
                    attrs={"property": "og:description"}))
    if d_meta:
        description = d_meta.attrs["content"]
    else:
        raise LotParseError("No Meta Info")
    title = (soup
             .find("meta",
                   attrs={"property": "og:title"}))
    title = " | ".join(title.split(" | ")[:2])
    return {"description": description,
            "title": title}

def lot_from_html(soup):
    d_div = soup.find("div", class_="lotdetail-description-text")
    if d_div:
        description = "\n".join(d_div.stripped_strings)
    else:
        raise LotParseError("Couldn't find info in html")

    a_div = soup.find("div", class_="lotdetail-guarantee")
    w_div = soup.find("div", class_="lotdetail-subtitle")
    if not (a_div and w_div):
        raise LotParseError("Couldn't generate title")
    title = f"{a_div.text} | {w_div.text}"
    res = {"description": description,
           "title": title}
    return res            

def parse_lot_detail(lot):
    print(f"Parsing {lot.url}")
    r = requests.get(lot.url, headers=HEADERS)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        print("Parsing data from ld+json")
        res = lot_from_json(soup)
    except LotParseError:
        try:
            print("ld+json failed, parsing data from meta tags")
            res = lot_from_meta(soup)
        except LotParseError:
            print("No meta tag info, parsing from html")
            res = lot_from_html(soup)
    if res:
        for attr, val in res.items():
            setattr(lot, attr, val)
    else:
        raise LotParseError("Could not find attributes in page")
    save_image(soup, lot)
    lot.collected = True
    lot.save()

def parse_lots():
    to_parse = AuctionLot.objects.filter(visited=False, 
                                         collected=False,
                                         sale_price__isnull=False)
    for lot in to_parse:
        try: 
            parse_lot_detail(lot)
            lot.collected = True
        except LotParseError as e:
            print(f"Parse failed - {e}")
            continue
        finally:
            lot.visited=True
            lot.save()
            time.sleep(5)

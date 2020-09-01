import scrapy
from bs4 import BeautifulSoup
from bs4 import Comment
from .. import items
from .. import utility_func


class MediumRentalSpider(scrapy.Spider):
    name = 'rentSpider'

    def start_requests(self):
        url = 'https://www.clasificadosonline.com/UDRentalsListingAdv.asp?RentalsPueblos=%25&Category=%25&Bedrooms=%25&LowPrice=0&HighPrice=9999999999999999&Area=&redirecturl=%2FUDRentalsListingAdvMap.asp&BtnSearchListing=Listado'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css("td[valign='middle'][align='left'][width='223'] a"):
            yield response.follow(a, callback=self.parse)
        for a in response.css("table.tbl-main-photo a"):
            yield response.follow(a, callback=self.announcement_parse)
        pass

    def announcement_parse(self, response):
        announcement = items.ForRentAnnouncement()
        announcement["for_rent_id"] = response.url.split("=")[1]
        announcement["name"] = response.css("span.Tah16nounder span.Ver14 strong::text").get()[:-2]
        announcement["price"] = response.css("span.Tahoma14Negro strong::text").get()
        announcement["category"] = response.css("table.translate div[align='center'] span.Tahoma14Brown::text").getall()[1].split(" ")[0]
        announcement["am_rooms"] = response.css("span.Tahoma14Brown strong")[0].css("::text").get()
        announcement["am_bathrooms"] = response.css("span.Tahoma14Brown strong")[1].css("::text").get()
        announcement["loc1"] = response.css("span.Tahoma14Negro a.Tahoma14")[0].css("::text").get()
        announcement["loc2"] = response.css("span.Tahoma14Negro a.Tahoma14")[1].css("::text").get()
        announcement["photo_urls"] = response.css("div.MagicScroll a").xpath("@href").getall()
        announcement["description"] = response.css("span.more.comment::text").get()
        if len(announcement["photo_urls"]) == 0:
            announcement["photo_urls"] = [response.css("#Trans").xpath("@href").get()]
        if announcement["photo_urls"] == [None]:
            announcement["photo_urls"] = None
        soup = BeautifulSoup(response.body, 'html.parser')
        lat_long_comment = soup.find_all(string=lambda text: isinstance(text, Comment))[41]
        lat_start_index = lat_long_comment.find('class="Lat" value=') + 19
        lat_length = 0
        for i in range(20):
            if lat_long_comment[lat_start_index + i] == '"':
                lat_length = i
                break
        announcement["lat"] = lat_long_comment[lat_start_index:lat_start_index + lat_length]
        if announcement["lat"] == "":
            announcement["lat"] = None
        lon_start_index = lat_long_comment.find('class="Lon" value=') + 19
        lon_length = 0
        for i in range(20):
            if lat_long_comment[lon_start_index + i] == '"':
                lon_length = i
                break
        announcement["lon"] = lat_long_comment[lon_start_index:lon_start_index + lon_length]
        if announcement["lon"] == "":
            announcement["lon"] = None

        image_seller = response.css("table[style='padding-bottom:4%'] img")
        if image_seller == list():
            announcement["seller_id"] = "OFR" + announcement["for_rent_id"]
            seller = items.ForRentSeller()
            seller["seller_id"] = "OFR" + announcement["for_rent_id"]
            seller["name"] = response.css("span.Tahoma14BrownNound::text").get()
            if seller["name"] is None:
                seller["name"] = response.css("font[color='#FF0000']::text").get()
            if seller["name"] is not None:
                seller["name"] = utility_func.strip2(seller["name"])
            seller["company"] = response.css("span.Tahoma14 a::text").get()
            if seller["company"] is not None:
                seller["company"] = seller["company"].strip()[:-2]
            seller["phone"] = response.css("div p span.Tahoma14Brown::text").get()
            seller["PartnersListingREFRID"] = None
            seller["address"] = None
            seller["website_url"] = None
            seller["lat"] = None
            seller["lon"] = None
            yield seller
        else:
            a_tag = image_seller.xpath("..")[0]
            partnersListingREFRID = a_tag.xpath("@href").get().split("=")[1]
            announcement["seller_id"] = "PLFR" + partnersListingREFRID
            name = response.css("span.Tahoma14BrownNound::text").get()
            if name is None:
                name = response.css("font[color='#FF0000']::text").get()
            if name is not None:
                name = utility_func.strip2(name)
            yield response.follow(a_tag, callback=self.seller_parse, meta={"name": name})

        for key, value in dict(announcement).items():
            if value is None and key != 'lat' and key != 'lon':
                print("Alert ", key)
        yield announcement

    def seller_parse(self, response):
        seller = items.ForRentSeller()
        seller['PartnersListingREFRID'] = response.url.split("=")[1]
        seller['seller_id'] = "PLFR" + seller['PartnersListingREFRID']
        seller['address'] = response.css("span.Tahoma14")[1].css("::text").get()[:-1]
        if seller['address'] is not None:
            seller['address'] = seller['address'].strip()
        seller['website_url'] = response.css("#websitesubstr::text").get()
        seller['company'] = response.css(
            "span.Tahoma14 font[face='Verdana, Arial, Helvetica, sans-serif'] b::text").get()
        seller['phone'] = response.css("font.Tahoma14azul::text").get()
        seller['lat'] = response.css("#Lat").xpath("@value").get()
        seller['lon'] = response.css("#Lon").xpath("@value").get()
        seller['name'] = response.meta["name"]
        yield seller

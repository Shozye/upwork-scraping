import scrapy

from .. import items


class BigSpanishSpider(scrapy.Spider):
    name = "spanishSpider"

    def start_requests(self):
        cities = ["%25"]
        for city in cities:
            url = f"https://www.clasificadosonline.com/UDREListing.asp?RESPueblos={city}&Category=%25&LowPrice=0&HighPrice=999999999&Bedrooms=%25&Area=&Repo=Repo&BtnSearchListing=Listado&redirecturl=%2Fudrelistingmap.asp"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css("td[valign='middle'][align='left'] a"):
            yield response.follow(a, callback=self.parse)
        for a in response.css("table.tbl-main-photo a"):
            if a.xpath("@href").get()[:20] == "/REFSMultipleSellers":
                yield response.follow(a, callback=self.multiple_seller_parse)
            else:
                yield response.follow(a, callback=self.announcement_parse)
            pass
        pass

    def multiple_seller_parse(self, response):
        estate_id = "MS" + response.url.split("=")[1]
        for a in response.css("[valign='middle'] a[target='_blank']"):
            yield response.follow(a, callback=self.announcement_parse, meta={"estate_id": estate_id})
        pass

    def announcement_parse(self, response):
        announcement = items.ClasificaEstateItem()
        announcement["announcement_id"] = response.css("strong a.style7::text").get()
        if response.meta.get('estate_id', None) is not None:
            announcement["estate_id"] = response.meta["estate_id"]
        else:
            announcement["estate_id"] = announcement["announcement_id"]
        announcement["name"] = response.css("span.Tahoma24nounder strong::text").get()
        announcement["price"] = response.css("span.Tah16nounder span.Tahoma14Negro strong::text").get()
        announcement["category"] = response.css("span span.Tahoma14Gris::text").get()[36:].strip()
        announcement["am_bedrooms"] = response.css("span.Tahoma14Brown span.Tahoma14Negro strong::text").getall()[0][
                                      :-2]
        announcement["am_bathrooms"] = response.css("span.Tahoma14Brown span.Tahoma14Negro strong::text").getall()[1]
        announcement["loc1"] = response.css("span.Tahoma14Negro a.Tahoma14::text").getall()[0]
        announcement["loc2"] = response.css("span.Tahoma14Negro a.Tahoma14::text").getall()[1]
        lat_long_src = response.css("#ifMap").xpath("@src").get().split("&")
        announcement["lat"] = lat_long_src[1][9:]
        announcement["long"] = lat_long_src[2][9:]
        announcement["photo_urls"] = response.css("div.MagicScroll a").xpath("@href").getall()
        announcement["description"] = response.css("span.more.comment::text").get()
        if len(announcement["photo_urls"]) == 0:
            announcement["photo_urls"] = [response.css("#Trans").xpath("@href").get()]
        if announcement["photo_urls"] == [None]:
            announcement["photo_urls"] = None

        image_seller = response.css("td.Ver12C img[itemprop='image']")
        if image_seller == list():
            announcement["seller_id"] = "O" + announcement["announcement_id"]
            seller = items.Seller()
            seller["seller_id"] = "O" + announcement["announcement_id"]
            seller["PartnersListingREID"] = None
            seller["description"] = None
            seller["name"] = response.css("div.translate span.Tahoma14BrownNound::text").get()
            seller["company"] = response.css("div.translate span.Tahoma14Brown a.Tahoma14::text").get()
            if seller["name"] is None:
                seller["name"] = response.css("span.Tahoma12Black span.Tahoma14Negro::text").get()
            seller["phone"] = response.css("div.translate span.Tahoma14::text").get()
            yield seller
        else:
            a_tag = image_seller.xpath("..")[0]
            partnersListingREID = a_tag.xpath("@href").get().split("=")[1]
            announcement["seller_id"] = "PL" + partnersListingREID
            yield response.follow(url=a_tag.xpath("@href").get(), callback=self.seller_parse)

        for key, value in dict(announcement).items():
            if value is None:
                print("Alert ", key)
        yield announcement

    def seller_parse(self, response):
        seller = items.Seller()
        seller["PartnersListingREID"] = response.url.split("=")[1]
        seller["seller_id"] = "PL" + seller["PartnersListingREID"]
        seller["name"] = None
        seller['company'] = response.css("span[itemprop='name'] strong::text").get()
        seller['phone'] = response.css("span[itemprop='telephone']::text").get()
        seller['postal_code'] = response.css("span[itemprop='postalCode']::text").get()
        seller['address_locality'] = response.css("span[itemprop='addressLocality']::text").get()[:-3]
        seller['address_region'] = response.css("span[itemprop='addressRegion']::text").get()
        seller['website_url'] = response.css("span[itemprop='url'] a").xpath("@href").get()
        seller["description"] = response.css("div[align='center'] span.Roboto::text").get()
        for key, value in dict(seller).items():
            if value is None and key != 'name':
                print("Alert ", key)
        yield seller

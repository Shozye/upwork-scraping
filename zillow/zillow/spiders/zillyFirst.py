import scrapy
import json
from .. import utility
from .. import items
from time import sleep
from .. import urls

class zillyFirst(scrapy.Spider):
    name = "zillyFirst"

    def __init__(self, n=None, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.n = n

    def start_requests(self):
        part = int(self.n)
        start_urls = [x['url'] for x in json.loads(urls.parts[part])]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.announcement_parse)

    def announcement_parse(self, response):
        try:
            script = json.loads(response.css("script#hdpApolloPreloadedData::text").get())
            zpid = script['zpid']
            key = f"""OffMarketDoubleScrollFullRenderQuery{{'zpid':{zpid},'contactFormRenderParameter':{{'zpid':{zpid},'platform':'desktop','isDoubleScroll':true}}}}"""
            try:
                details = json.loads(script['apiCache'].replace("\\\"", "'"))[key]['property']
            except (TypeError, KeyError):
                key2 = f"""ForSaleDoubleScrollFullRenderQuery{{'zpid':{zpid},'contactFormRenderParameter':{{'zpid':{zpid},'platform':'desktop','isDoubleScroll':true}}}}"""
                details = json.loads(script['apiCache'].replace("\\\"", "'"))[key2]['property']
            listing = items.Listing()
            listing["zpid"] = details["zpid"]
            listing["country"] = details["country"]
            listing["state"] = details["state"]
            listing["city"] = details["city"]
            listing["zipcode"] = details["zipcode"]
            listing["street_address"] = details["streetAddress"]

            listing["last_sold_price"] = details["lastSoldPrice"]
            listing["year_built"] = details["yearBuilt"]
            listing["am_bedrooms"] = details["bedrooms"]
            listing["am_bathrooms"] = details["bathrooms"]
            listing["living_area"] = details["livingAreaValue"]
            listing["lot_area"] = details["lotAreaValue"]
            listing["home_type"] = details["homeType"]
            photo_urls = list()
            for dictionary in details["responsivePhotosOriginalRatio"]:
                photo_urls.append(dictionary['mixedSources']['webp'][-1]['url'])
            listing["photo_urls"] = photo_urls
            listing["latitude"] = details["latitude"]
            listing["longitude"] = details["longitude"]

            listing["description"] = details["description"]
            price_history = details["priceHistory"]
            for i in range(len(price_history)):
                dic = price_history[i]
                del dic['showCountyLink']
                del dic['postingIsRental']
                del dic['attributeSource']
                try:
                    dic['buyerAgent'] = dic['buyerAgent']['profileUrl']
                except (KeyError, TypeError):
                    dic['buyerAgent'] = None
                try:
                    dic['sellerAgent'] = dic['sellerAgent']['profileUrl']
                except (KeyError, TypeError):
                    dic['sellerAgent'] = None
            listing["price_history"] = price_history
            listing["home_status"] = details["homeStatus"]
            yield listing
        except TypeError:
            if 'captchaPerimeterX' in response.url:
                self.logger.error(f"got captcha'd in {response.url}")
                yield scrapy.Request(response.url, callback=self.announcement_parse, dont_filter=True)
            else:
                raise Exception("No captcha perimeter in link and TypeError")

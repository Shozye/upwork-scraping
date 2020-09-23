import scrapy
import json
from .. import utility
from .. import items

class zillySpider(scrapy.Spider):
    name = "zillySpider"

    def start_requests(self):
        place = "Puerto Rico"
        # place = "Texas"
        url, meta = utility.create_search_link_meta(place,
                                                    min_price=0,
                                                    max_price=1000000000,  # max_price=1000000000,
                                                    min_lot_size=0,
                                                    max_lot_size=5000000)
        yield scrapy.Request(url, callback=self.search_parse,
                             meta=meta)

    def search_parse(self, response):
        amount_results = int(
            response.css("span.result-count::text").get().split(" ")[0].replace(",", "")) if response.css(
            "span.result-count::text").get() is not None else 0
        meta = response.meta
        if amount_results > 500:
            if meta.get('min_lot_size', 1) != 0 or meta.get('max_lot_size', 1) != 5000000:
                if meta['max_lot_size'] - meta['min_lot_size'] < 100:
                    raise Exception(
                        f"UNABLE TO FILTER OUT {meta['place']}, {meta['min_price']}, {meta['max_price']}, {meta['min_lot_size']}, {meta['max_lot_size']}")
                else:
                    url1, meta1 = utility.create_search_link_meta(meta['place'],
                                                                  meta['min_price'],
                                                                  meta['max_price'],
                                                                  meta['min_lot_size'],
                                                                  (meta['max_lot_size'] + meta['min_lot_size']) // 2)
                    url2, meta2 = utility.create_search_link_meta(meta['place'],
                                                                  meta['min_price'],
                                                                  meta['max_price'],
                                                                  (meta['min_lot_size'] + meta[
                                                                      'max_lot_size']) // 2 + 1,
                                                                  meta['max_lot_size'])
            else:
                if meta['max_price'] - meta['min_price'] < 100:
                    url1, meta1 = utility.create_search_link_meta(meta['place'],
                                                                  meta['min_price'],
                                                                  meta['max_price'],
                                                                  meta['min_lot_size'],
                                                                  (meta['max_lot_size'] + meta['min_lot_size']) // 2)
                    url2, meta2 = utility.create_search_link_meta(meta['place'],
                                                                  meta['min_price'],
                                                                  meta['max_price'],
                                                                  (meta['min_lot_size'] + meta[
                                                                      'max_lot_size']) // 2 + 1,
                                                                  meta['max_lot_size'])
                else:
                    url1, meta1 = utility.create_search_link_meta(meta['place'],
                                                                  meta['min_price'],
                                                                  (meta['min_price'] + meta['max_price']) // 2,
                                                                  meta['min_lot_size'],
                                                                  meta['max_lot_size'])
                    url2, meta2 = utility.create_search_link_meta(meta['place'],
                                                                  (meta['min_price'] + meta['max_price']) // 2 + 1,
                                                                  meta['max_price'],
                                                                  meta['min_lot_size'],
                                                                  meta['max_lot_size'])
            yield scrapy.Request(url1, callback=self.search_parse, meta=meta1)
            yield scrapy.Request(url2, callback=self.search_parse, meta=meta2)
        elif 0 < amount_results <= 500:
            if response.css("li.PaginationNumberItem-bnmlxt-0 a::text").get() is not None:
                am_pages = int(response.css("li.PaginationNumberItem-bnmlxt-0 a::text").getall()[-1].replace('"', ''))
            else:
                am_pages = 1
            for page_num in range(1, am_pages + 1):
                url, new_meta = utility.create_search_link_meta(meta['place'], meta['min_price'], meta['max_price'],
                                                                meta['min_lot_size'], meta['max_lot_size'], page_num)
                yield scrapy.Request(url, callback=self.listing_parse, meta=new_meta, dont_filter=True)
        else:
            self.logger.debug(f"No listings on {response.url}")

    def listing_parse(self, response):
        for a in response.css("a.list-card-img"):
            yield response.follow(a, callback=self.announcement_parse)

    def announcement_parse(self, response):
        script = json.loads(response.css("script#hdpApolloPreloadedData::text").get())
        zpid = script['zpid']
        key = f"""OffMarketDoubleScrollFullRenderQuery{{'zpid':{zpid},'contactFormRenderParameter':{{'zpid':{zpid},'platform':'desktop','isDoubleScroll':true}}}}"""
        details = json.loads(script['apiCache'].replace("\\\"", "'"))[key]['property']
        """ 
        with open("script.txt", 'w+', encoding='utf-8') as file:
            file.write(json.dumps(details))
        """
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
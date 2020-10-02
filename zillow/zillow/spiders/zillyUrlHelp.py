import scrapy
import json
from .. import utility
from .. import items
from time import sleep
from .. import counties
from .. import add_urls

class zillyUrlHelp(scrapy.Spider):
    name = "zillyurlhelp"

    def start_requests(self):
        # place = "Puerto Rico"
        for url in add_urls.urls:
            for link in utility.create_4_special_search_links(url["place"], url["min_price"], url["max_price"], url["min_lot_size"], url["max_lot_size"]):
                new_url, meta = link[0], link[1]
                print(meta)
                yield scrapy.Request(new_url, callback=self.search_parse, meta=meta)
    def search_parse(self, response):
        try:
            amount_script = response.css("script[data-zrr-shared-data-key='mobileSearchPageStore']::text").get()
            amount_results = json.loads(amount_script[4:-3])["cat1"]["searchList"]["totalResultCount"]
            meta = response.meta
            self.logger.info(f"{amount_results} on site {response.url}")
            if amount_results > 750:
                self.logger.error(f"problem because we need more links {response.url}")
                pass
            elif 0 < amount_results <= 750:
                if response.css("li.PaginationNumberItem-bnmlxt-0 a::text").get() is not None:
                    am_pages = int(
                        response.css("li.PaginationNumberItem-bnmlxt-0 a::text").getall()[-1].replace('"', ''))
                else:
                    am_pages = 1
                for page_num in range(1, am_pages + 1):
                    url, new_meta = utility.create_special_search_link(meta['place'], meta['min_price'], meta['max_price'],
                                                                    meta['min_lot_size'], meta['max_lot_size'],
                                                                    page_num, meta['min_sqft'], meta['max_sqft'])
                    yield scrapy.Request(url, callback=self.listing_parse, meta=new_meta, dont_filter=True)
            else:
                self.logger.info(f"No listings on {response.url}")
        except TypeError:
            if 'captchaPerimeterX' in response.url:
                meta = response.meta
                url1, meta1 = utility.create_search_link_meta(meta['place'],
                                                              meta['min_price'],
                                                              meta['max_price'],
                                                              meta['min_lot_size'],
                                                              meta['max_lot_size'])
                self.logger.error(f"got captcha'd in {response.url}")
                yield scrapy.Request(url1, callback=self.search_parse, meta=meta1, dont_filter=True)
            else:
                raise Exception("No captcha perimeter in link and TypeError")

    def listing_parse(self, response):
        if 'captchaPerimeterX' not in response.url:
            for a in response.css("a.list-card-img").xpath("@href").getall():
                announcement = items.Announcement()
                announcement["url"] = a
                yield announcement
                # yield response.follow(a, callback=self.announcement_parse)
        else:
            self.logger.error(f"got captcha'd in {response.url}")
            yield scrapy.Request(response.url, callback=self.listing_parse, dont_filter=True)
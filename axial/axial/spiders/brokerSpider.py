import scrapy
from .. import items


class brokerSpider(scrapy.Spider):
    name = "broky"
    huge_amount = 0

    def start_requests(self):
        for i in range(1, 83):
            url = f"https://www.axial.net/forum/companies/united-states-business-brokers/{i}/"
            yield scrapy.Request(url, callback=self.url_parse)

    def url_parse(self, response):
        print(response.css("a.teaser1-wrap").getall())
        for a in response.css("a.teaser1-wrap").xpath("@href").getall():
            item = items.Url()
            item['url'] = a
            yield item

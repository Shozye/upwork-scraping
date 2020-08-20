# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClasificaEstateItem(scrapy.Item):
    announcement_id = scrapy.Field()
    main_photo_url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    am_bedrooms = scrapy.Field()
    am_bathrooms = scrapy.Field()
    loc1 = scrapy.Field()
    loc2 = scrapy.Field()
    lat = scrapy.Field()
    long = scrapy.Field()
    photo_urls = scrapy.Field()
    seller_name = scrapy.Field()
    seller_phone = scrapy.Field()
    description = scrapy.Field()
    pass

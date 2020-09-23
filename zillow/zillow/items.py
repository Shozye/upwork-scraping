# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Listing(scrapy.Item):
    # define the fields for your item here like:
    zpid = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()

    last_sold_price = scrapy.Field()
    year_built = scrapy.Field()
    zipcode = scrapy.Field()
    street_address = scrapy.Field()
    am_bedrooms = scrapy.Field()
    am_bathrooms = scrapy.Field()
    living_area = scrapy.Field()
    lot_area = scrapy.Field()
    home_type = scrapy.Field()
    photo_urls = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    description = scrapy.Field()
    price_history = scrapy.Field()
    home_status = scrapy.Field()

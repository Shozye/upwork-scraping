# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Listing(scrapy.Item):
    unit_id = scrapy.Field()
    title = scrapy.Field()
    property_type = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    sleeps = scrapy.Field()
    area_value = scrapy.Field()
    rating = scrapy.Field()
    am_reviews = scrapy.Field()
    page_url = scrapy.Field()
    all_photo_url = scrapy.Field()
    price = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

class DetailPage(scrapy.Item):
    unit_id = scrapy.Field()
    title = scrapy.Field()
    property_type = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    sleeps = scrapy.Field()
    area_value = scrapy.Field()
    area_units = scrapy.Field()
    rating = scrapy.Field()
    am_reviews = scrapy.Field()
    page_url = scrapy.Field()
    address_city = scrapy.Field()
    address_country = scrapy.Field()
    postal_code = scrapy.Field()
    state_province = scrapy.Field()
    all_photo_url = scrapy.Field()
    features = scrapy.Field()
    price_amount = scrapy.Field()
    price_currency = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    availability_begin = scrapy.Field()
    availability_end = scrapy.Field()
    availability_min_stay_default = scrapy.Field()
    availability_string = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ForSaleAnnouncement(scrapy.Item):
    announcement_id = scrapy.Field()
    estate_id = scrapy.Field()
    seller_id = scrapy.Field()
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
    description = scrapy.Field()
    pass


class ForSaleSeller(scrapy.Item):
    seller_id = scrapy.Field()
    PartnersListingREID = scrapy.Field()
    address_locality = scrapy.Field()
    address_region = scrapy.Field()
    postal_code = scrapy.Field()
    website_url = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    phone = scrapy.Field()
    description = scrapy.Field()

class ForRentSeller(scrapy.Item):
    seller_id = scrapy.Field()
    PartnersListingREFRID = scrapy.Field()
    address = scrapy.Field()
    website_url = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    phone = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()


class VacRentalAnnouncement(scrapy.Item):
    vacation_id = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    city = scrapy.Field()
    rate_night = scrapy.Field()
    amount_of_rooms = scrapy.Field()
    website_url = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    photo_urls = scrapy.Field()
    description = scrapy.Field()

class ForRentAnnouncement(scrapy.Item):
    for_rent_id = scrapy.Field()
    seller_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    am_rooms = scrapy.Field()
    am_bathrooms = scrapy.Field()
    loc1 = scrapy.Field()
    loc2 = scrapy.Field()
    photo_urls = scrapy.Field()
    description = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    pass
import scrapy.http.response
import json


class ListingDictParser:
    def __init__(self, avail_dict):
        # response is scrapy response object
        self.avail_dict = avail_dict
        pass

    def unit_id(self):
        return self.avail_dict['propertyId']

    def title(self):
        return self.avail_dict['propertyMetadata']['headline']

    def property_type(self):
        return self.avail_dict['propertyType']

    def bedrooms(self):
        return self.avail_dict['bedrooms']

    def bathrooms(self):
        return self.avail_dict['bathrooms']['full']

    def sleeps(self):
        return self.avail_dict['sleeps']

    def area_value(self):
        return self.avail_dict['spaces']['spacesSummary']['area']['areaValue']

    def rating(self):
        return self.avail_dict['averageRating']

    def am_reviews(self):
        return self.avail_dict['reviewCount']

    def page_url(self):
        return self.avail_dict['detailPageUrl']

    def all_photo_url(self):
        d = self.avail_dict['images']
        images = [x['c6_uri'] for x in d]
        return images

    def price(self):
        return self.avail_dict['priceSummary']['formattedAmount']

    def latitude(self):
        return self.avail_dict['geoCode']['latitude']

    def longitude(self):
        return self.avail_dict['geoCode']['longitude']

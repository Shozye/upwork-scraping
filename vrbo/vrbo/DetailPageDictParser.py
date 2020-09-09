import scrapy.http.response
import json


class DetailPageDictParser:
    def __init__(self, response):
        # response is scrapy response object
        self.response = response
        self.avail_dict = self.get_info_dict()
        pass

    def get_info_dict(self):
        script = self.response.css("body script::text")[0].get()
        try:
            dictionary = json.loads(script.split('window.__INITIAL_STATE__ = ')[1].split('};')[0]+"}")
        except json.decoder.JSONDecodeError:
            with open('jsondecoder.txt','w+', encoding='utf-8') as file:
                file.write(script.split('window.__INITIAL_STATE__ = ')[1].split('};')[0]+"}")
            raise
        return dictionary

    def unit_id(self):
        return self.avail_dict['listingReducer']['listingNumber']

    def title(self):
        return self.avail_dict['listingReducer']['headline']

    def property_type(self):
        return self.avail_dict['listingReducer']['propertyType']

    def bedrooms(self):
        return self.avail_dict['listingReducer']['bedrooms']

    def bathrooms(self):
        return self.avail_dict['listingReducer']['bathrooms']['full'] + self.avail_dict['listingReducer']['bathrooms'][
            'half']

    def sleeps(self):
        return self.avail_dict['listingReducer']['sleeps']

    def area_value(self):
        return self.avail_dict['listingReducer']['spaces']['spacesSummary']['area']['areaValue']

    def area_units(self):
        return self.avail_dict['listingReducer']['spaces']['spacesSummary']['area']['areaUnits']

    def rating(self):
        return self.avail_dict['reviewsReducer']['averageRating']

    def am_reviews(self):
        return self.avail_dict['reviewsReducer']['reviewCount']

    def page_url(self):
        return self.avail_dict['listingReducer']['detailPageUrl']

    def address_city(self):
        return self.avail_dict['listingReducer']['address']['city']

    def address_country(self):
        return self.avail_dict['listingReducer']['address']['country']

    def postal_code(self):
        return self.avail_dict['listingReducer']['address']['postalCode']

    def state_province(self):
        return self.avail_dict['listingReducer']['address']['stateProvince']

    def all_photo_url(self):
        d = self.avail_dict['listingReducer']['images']
        images = [x['uri'] for x in d]
        return images

    def features(self):
        return self.avail_dict['listingReducer']['allFeaturedAmenitiesRanked']

    def price_amount(self):
        try:
            return self.avail_dict['listingReducer']['priceSummary']['amount']
        except KeyError:
            return None

    def price_currency(self):
        try:
            return self.avail_dict['listingReducer']['priceSummary']['currency']
        except KeyError:
            return None

    def latitude(self):
        return self.avail_dict['listingReducer']['geoCode']['latitude']

    def longitude(self):
        return self.avail_dict['listingReducer']['geoCode']['longitude']

    def availability_begin(self):
        return self.avail_dict['listingReducer']['availabilityCalendar']['availability']['dateRange']['beginDate']

    def availability_end(self):
        return self.avail_dict['listingReducer']['availabilityCalendar']['availability']['dateRange']['endDate']

    def availability_min_stay_default(self):
        return self.avail_dict['listingReducer']['availabilityCalendar']['availability']['minStayDefault']

    def availability_string(self):
        return self.avail_dict['listingReducer']['availabilityCalendar']['availability']['unitAvailabilityConfiguration']['availability']


import scrapy
import json
from .. import items
from .. import ListingDictParser
from .. import filters
from .. import DetailPageDictParser


class HomeSpider(scrapy.Spider):
    name = "vrboSpider"

    def start_requests(self):
        countries = ["alabama-united-states-of-america", "alaska-united-states-of-america", "arizona-united-states-of-america", "arkansas-united-states-of-america", "california-united-states-of-america", "colorado-united-states-of-america", "connecticut-united-states-of-america", "delaware-united-states-of-america", "florida-united-states-of-america", "georgia-united-states-of-america", "hawaii-united-states-of-america", "idaho-united-states-of-america", "illinois-united-states-of-america", "indiana-united-states-of-america", "iowa-united-states-of-america", "kansas-united-states-of-america", "kentucky-united-states-of-america", "louisiana-united-states-of-america", "maine-united-states-of-america", "maryland-united-states-of-america", "massachusetts-united-states-of-america", "michigan-united-states-of-america", "minnesota-united-states-of-america", "mississippi-united-states-of-america", "missouri-united-states-of-america", "montana-united-states-of-america", "nebraska-united-states-of-america", "nevada-united-states-of-america", "new-hampshire-united-states-of-america", "new-jersey-united-states-of-america", "new-mexico-united-states-of-america", "new-york-united-states-of-america", "north-carolina-united-states-of-america", "north-dakota-united-states-of-america", "ohio-united-states-of-america", "oklahoma-united-states-of-america", "oregon-united-states-of-america", "pennsylvania-united-states-of-america", "rhode-island-united-states-of-america", "south-carolina-united-states-of-america", "south-dakota-united-states-of-america", "tennessee-united-states-of-america", "texas-united-states-of-america", "utah-united-states-of-america", "vermont-united-states-of-america", "virginia-united-states-of-america", "washington-united-states-of-america", "west-virginia-united-states-of-america", "wisconsin-united-states-of-america", "wyoming-united-states-of-america", "afghanistan", "albania", "algeria", "andorra", "angola", "antigua-and-barbuda", "argentina", "armenia", "australia", "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan", "bolivia", "bosnia-and-herzegovina", "botswana", "brazil", "brunei-darussalam", "bulgaria", "burkina-faso", "burundi", "cabo-verde", "cambodia", "cameroon", "canada", "central-african-republic", "chad", "chile", "china", "colombia", "comoros", "congo", "cook-islands", "costa-rica", "croatia", "cuba", "cyprus", "czechia", "cote-divoire", "denmark", "dominica", "dominican-republic", "ecuador", "egypt", "el-salvador", "eritrea", "estonia", "eswatini", "ethiopia", "faroe-islands-", "fiji", "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana", "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", "indonesia", "iran", "iraq", "ireland", "israel", "italy", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "kuwait", "kyrgyzstan", "latvia", "lebanon", "lesotho", "liberia", "libya", "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall-islands", "mauritania", "mauritius", "mexico", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands", "new-zealand", "nicaragua", "niger", "nigeria", "niue", "north-macedonia", "norway", "oman", "pakistan", "palau", "panama", "papua-new-guinea", "paraguay", "peru", "philippines", "poland", "portugal", "qatar", "south-korea", "moldova", "romania", "russia", "rwanda", "st-kitts-and-nevis", "saint-lucia", "saint-vincent-and-the-grenadines", "samoa", "san-marino", "sao-tome-and-principe", "saudi-arabia", "senegal", "serbia", "seychelles", "sierra-leone", "singapore", "slovakia", "slovenia", "solomon-islands", "somalia", "south-africa", "south-sudan", "spain", "sri-lanka", "sudan", "suriname", "sweden", "switzerland", "syrian-arab-republic", "tajikistan", "thailand", "timor-leste", "togo", "tokelau", "tonga", "trinidad-and-tobago", "tunisia", "turkey", "turkmenistan", "uganda", "ukraine", "united-arab-emirates", "united-kingdom", "tanzania", "uruguay", "uzbekistan", "vanuatu", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe"]
        countries = ['florida-united-states-of-america']
        for country_name in countries:
            yield self.yield_begin_parse(country_name, [])

    def begin_parse(self, response):
        # loc, prop, nearby

        data = json.loads(response.body)
        am_results = data['data']['results']['resultCount']
        how_many_pages = data['data']['results']['pageCount']
        _filters = json.loads(response.request._body)['variables']['request']['filters']
        am_bedrooms = json.loads(response.request._body)['variables']['request']['coreFilters']['maxBedrooms']
        am_bathrooms = json.loads(response.request._body)['variables']['request']['coreFilters']['maxBathrooms']
        country_name = json.loads(response.request._body)['variables']['request']['q']
        price_min = json.loads(response.request._body)['variables']['request']['coreFilters']['minPrice']
        if am_results == 0:
            pass
        elif am_results <= 1000:
            for i in range(1, how_many_pages + 1):
                yield self.yield_listing_parse(country_name, _filters, i, am_bedrooms=am_bedrooms,
                                               am_bathrooms=am_bathrooms, price=price_min)
        else:
            if price_min == 0 or price_min is None:
                for i in range(1, 992, 10):
                    price_min = i
                    yield self.yield_begin_parse(country_name, [], am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            elif am_bedrooms is None:
                for i in range(1, 50):
                    am_bedrooms = i
                    yield self.yield_begin_parse(country_name, [], am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            elif am_bathrooms is None:
                for i in range(1, 50):
                    am_bathrooms = i
                    yield self.yield_begin_parse(country_name, [], am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            elif len(_filters) == 0:
                for i in filters.location:
                    fltr = [prev_filter for prev_filter in
                            json.loads(response.request._body)['variables']['request']['filters']]
                    fltr.append(i)
                    yield self.yield_begin_parse(country_name, fltr, am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            elif len(_filters) == 1:
                for i in filters.property_type:
                    fltr = [prev_filter for prev_filter in
                            json.loads(response.request._body)['variables']['request']['filters']]
                    fltr.append(i)
                    yield self.yield_begin_parse(country_name, fltr, am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            elif len(_filters) == 2:
                for i in filters.nearby_activities:
                    fltr = [prev_filter for prev_filter in
                            json.loads(response.request._body)['variables']['request']['filters']]
                    fltr.append(i)
                    yield self.yield_begin_parse(country_name, fltr, am_bedrooms=am_bedrooms, am_bathrooms=am_bathrooms,
                                                 price=price_min)
            else:
                print("HOUSTON WE HAVE GOT A PROBLEM\n", country_name, _filters, "am_results=", am_results,
                      "am_bedrooms", am_bedrooms, "am_bathrooms", am_bathrooms, "price", price_min)
                raise Exception("HOUSTON, WE HAVE GOT A PROBLEM :(")

            pass

    def yield_listing_parse(self, country, filters, page_num, am_bedrooms=None, am_bathrooms=None, price=0):

        am_bedrooms_max, am_bedrooms_min = am_bedrooms, am_bedrooms
        if am_bedrooms is None:
            am_bedrooms_max = None
            am_bedrooms_min = 0
        am_bathrooms_max, am_bathrooms_min = am_bathrooms, am_bathrooms
        if am_bathrooms is None:
            am_bathrooms_max = None
            am_bathrooms_min = 0
        price_max, price_min = price + 19, price
        if price is None or price == 0:
            price_max = None
            price_min = 0
        elif price_max == 1000:
            price_max = None
        # print(country, filters, am_bathrooms_min, am_bathrooms_max, price_min, price_max, am_bedrooms_min, am_bedrooms_max, page_num)
        data = {"operationName": "SearchRequestQuery", "variables": {"filterCounts": True,
                                                                     "request": {
                                                                         "paging": {"page": page_num,
                                                                                    "pageSize": 50},
                                                                         "coreFilters": {"adults": 1,
                                                                                         "maxBathrooms": am_bathrooms_max,
                                                                                         "maxBedrooms": am_bedrooms_max,
                                                                                         "maxPrice": price_max,
                                                                                         "minBathrooms": am_bathrooms_min,
                                                                                         "minBedrooms": am_bedrooms_min,
                                                                                         "minPrice": price_min,
                                                                                         "pets": 0},
                                                                         "filters": filters,
                                                                         "q": country},
                                                                     "vrbo_web_global_messaging_alert": True,
                                                                     "vrbo_web_global_messaging_banner": True},
                "extensions": {"isPageLoadSearch": False},
                "query": "query SearchRequestQuery($request: SearchResultRequest!, $filterCounts: Boolean!, $vrbo_web_global_messaging_alert: Boolean!, $vrbo_web_global_messaging_banner: Boolean!) {\n  results: search(request: $request) {\n    id\n    typeaheadSuggestion {\n      uuid\n      term\n      name\n      __typename\n    }\n    geography {\n      lbsId\n      gaiaId\n      location {\n        latitude\n        longitude\n        __typename\n      }\n      isGeocoded\n      shouldShowMapCentralPin\n      __typename\n    }\n    propertyRedirectUrl\n    ...DestinationBreadcrumbsSearchResult\n    ...DestinationMessageSearchResult\n    ...FilterCountsSearchRequestResult\n    ...HitCollectionSearchResult\n    ...ADLSearchResult\n    ...MapSearchResult\n    ...ExpandedGroupsSearchResult\n    ...PagerSearchResult\n    ...SearchTermCarouselSearchResult\n    ...InternalToolsSearchResult\n    ...SEOMetaDataParamsSearchResult\n    ...GlobalInlineMessageSearchResult @include(if: $vrbo_web_global_messaging_alert)\n    ...GlobalBannerContainerSearchResult @include(if: $vrbo_web_global_messaging_banner)\n    __typename\n  }\n  ...RequestMarkerFragment\n}\n\nfragment DestinationBreadcrumbsSearchResult on SearchResult {\n  destination {\n    breadcrumbs {\n      name\n      url\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HitCollectionSearchResult on SearchResult {\n  page\n  pageSize\n  listings {\n    ...HitListing\n    __typename\n  }\n  pinnedListing {\n    listing {\n      availabilityInfo {\n        status\n        __typename\n      }\n      ...HitListing\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HitListing on Listing {\n  virtualTourBadge {\n    name\n    id\n    helpText\n    __typename\n  }\n  amenitiesBadges {\n    name\n    id\n    helpText\n    __typename\n  }\n  multiUnitProperty\n  images {\n    altText\n    c6_uri\n    c9_uri\n    __typename\n  }\n  listingNamespace\n  ...HitInfoListing\n  __typename\n}\n\nfragment HitInfoListing on Listing {\n  ...DetailsListing\n  ...PriceListing\n  ...RatingListing\n  ...GeoDistanceListing\n  detailPageUrl\n  instantBookable\n  minStayRange {\n    minStayHigh\n    minStayLow\n    __typename\n  }\n  listingId\n  rankedBadges(rankingStrategy: SERP) {\n    id\n    helpText\n    name\n    __typename\n  }\n  propertyId\n  listingNumber\n  propertyType\n  propertyMetadata {\n    headline\n    propertyName\n    __typename\n  }\n  superlativesBadges: rankedBadges(rankingStrategy: SERP_SUPERLATIVES) {\n    id\n    helpText\n    name\n    __typename\n  }\n  unitMessage(assetVersion: 1) {\n    iconText {\n      message\n      icon\n      messageValueType\n      __typename\n    }\n    __typename\n  }\n  unitMetadata {\n    unitName\n    __typename\n  }\n  __typename\n}\n\nfragment DetailsListing on Listing {\n  bathrooms {\n    full\n    half\n    toiletOnly\n    __typename\n  }\n  bedrooms\n  propertyType\n  sleeps\n  petsAllowed\n  spaces {\n    spacesSummary {\n      area {\n        areaValue\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PriceListing on Listing {\n  priceSummary: priceSummary {\n    priceTypeId\n    edapEventJson\n    formattedAmount\n    roundedFormattedAmount\n    pricePeriodDescription\n    priceAccurate\n    __typename\n  }\n  priceSummarySecondary: priceSummary(summary: \"displayPriceSecondary\") {\n    priceTypeId\n    edapEventJson\n    formattedAmount\n    roundedFormattedAmount\n    pricePeriodDescription\n    __typename\n  }\n  priceLabel: priceSummary(summary: \"priceLabel\") {\n    priceTypeId\n    pricePeriodDescription\n    __typename\n  }\n  __typename\n}\n\nfragment RatingListing on Listing {\n  averageRating\n  reviewCount\n  __typename\n}\n\nfragment GeoDistanceListing on Listing {\n  geoDistance {\n    text\n    relationType\n    __typename\n  }\n  __typename\n}\n\nfragment ExpandedGroupsSearchResult on SearchResult {\n  expandedGroups {\n    ...ExpandedGroupExpandedGroup\n    __typename\n  }\n  __typename\n}\n\nfragment ExpandedGroupExpandedGroup on ExpandedGroup {\n  listings {\n    ...HitListing\n    ...MapHitListing\n    __typename\n  }\n  mapViewport {\n    neLat\n    neLong\n    swLat\n    swLong\n    __typename\n  }\n  __typename\n}\n\nfragment MapHitListing on Listing {\n  ...HitListing\n  geoCode {\n    latitude\n    longitude\n    __typename\n  }\n  __typename\n}\n\nfragment FilterCountsSearchRequestResult on SearchResult {\n  id\n  resultCount\n  filterGroups {\n    groupInfo {\n      name\n      id\n      __typename\n    }\n    filters {\n      count @include(if: $filterCounts)\n      checked\n      filter {\n        id\n        name\n        refineByQueryArgument\n        description\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MapSearchResult on SearchResult {\n  mapViewport {\n    neLat\n    neLong\n    swLat\n    swLong\n    __typename\n  }\n  page\n  pageSize\n  listings {\n    ...MapHitListing\n    __typename\n  }\n  pinnedListing {\n    listing {\n      ...MapHitListing\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PagerSearchResult on SearchResult {\n  fromRecord\n  toRecord\n  pageSize\n  pageCount\n  page\n  resultCount\n  __typename\n}\n\nfragment DestinationMessageSearchResult on SearchResult {\n  destinationMessage(assetVersion: 4) {\n    iconTitleText {\n      title\n      message\n      icon\n      messageValueType\n      link {\n        linkText\n        linkHref\n        __typename\n      }\n      __typename\n    }\n    iconText {\n      message\n      icon\n      messageValueType\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ADLSearchResult on SearchResult {\n  parsedParams {\n    q\n    coreFilters {\n      adults\n      children\n      pets\n      minBedrooms\n      maxBedrooms\n      minBathrooms\n      maxBathrooms\n      minPrice\n      maxPrice\n      minSleeps\n      __typename\n    }\n    dates {\n      arrivalDate\n      departureDate\n      __typename\n    }\n    sort\n    __typename\n  }\n  page\n  pageSize\n  pageCount\n  resultCount\n  fromRecord\n  toRecord\n  pinnedListing {\n    listing {\n      listingId\n      __typename\n    }\n    __typename\n  }\n  listings {\n    listingId\n    __typename\n  }\n  filterGroups {\n    filters {\n      checked\n      filter {\n        groupId\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  geography {\n    lbsId\n    name\n    description\n    location {\n      latitude\n      longitude\n      __typename\n    }\n    primaryGeoType\n    breadcrumbs {\n      name\n      countryCode\n      location {\n        latitude\n        longitude\n        __typename\n      }\n      primaryGeoType\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RequestMarkerFragment on Query {\n  requestmarker\n  __typename\n}\n\nfragment SearchTermCarouselSearchResult on SearchResult {\n  discoveryXploreFeeds {\n    results {\n      id\n      title\n      items {\n        ... on SearchDiscoveryFeedItem {\n          type\n          imageHref\n          place {\n            uuid\n            name {\n              full\n              simple\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  typeaheadSuggestion {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InternalToolsSearchResult on SearchResult {\n  internalTools {\n    searchServiceUrl\n    __typename\n  }\n  __typename\n}\n\nfragment SEOMetaDataParamsSearchResult on SearchResult {\n  page\n  resultCount\n  pageSize\n  geography {\n    name\n    lbsId\n    breadcrumbs {\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalInlineMessageSearchResult on SearchResult {\n  globalMessages {\n    ...GlobalInlineAlertGlobalMessages\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalInlineAlertGlobalMessages on GlobalMessages {\n  alert {\n    action {\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    body {\n      text {\n        value\n        __typename\n      }\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    severity\n    title {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalBannerContainerSearchResult on SearchResult {\n  globalMessages {\n    ...GlobalBannerGlobalMessages\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalBannerGlobalMessages on GlobalMessages {\n  banner {\n    body {\n      text {\n        value\n        __typename\n      }\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    severity\n    title {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}

        return scrapy.http.JsonRequest(
            "https://www.vrbo.com/serp/g",
            callback=self.listing_parse, data=data)

        pass

    def yield_begin_parse(self, country, filters, am_bedrooms=None, am_bathrooms=None, price=0):

        am_bedrooms_max, am_bedrooms_min = am_bedrooms, am_bedrooms
        if am_bedrooms is None:
            am_bedrooms_max = None
            am_bedrooms_min = 0
        am_bathrooms_max, am_bathrooms_min = am_bathrooms, am_bathrooms
        if am_bathrooms is None:
            am_bathrooms_max = None
            am_bathrooms_min = 0
        price_max, price_min = price + 9, price
        if price is None or price == 0:
            price_max = None
            price_min = 0
        elif price_max >= 1000:
            price_max = None
        data = {"operationName": "SearchRequestQuery", "variables": {"filterCounts": True,
                                                                     "request": {
                                                                         "paging": {"page": 1, "pageSize": 50},
                                                                         "coreFilters": {"adults": 1,
                                                                                         "maxBathrooms": am_bathrooms_max,
                                                                                         "maxBedrooms": am_bedrooms_max,
                                                                                         "maxPrice": price_max,
                                                                                         "minBathrooms": am_bathrooms_min,
                                                                                         "minBedrooms": am_bedrooms_min,
                                                                                         "minPrice": price_min,
                                                                                         "pets": 0},
                                                                         "filters": filters,
                                                                         "q": country},
                                                                     "vrbo_web_global_messaging_alert": True,
                                                                     "vrbo_web_global_messaging_banner": True},
                "extensions": {"isPageLoadSearch": False},
                "query": "query SearchRequestQuery($request: SearchResultRequest!, $filterCounts: Boolean!, $vrbo_web_global_messaging_alert: Boolean!, $vrbo_web_global_messaging_banner: Boolean!) {\n  results: search(request: $request) {\n    id\n    typeaheadSuggestion {\n      uuid\n      term\n      name\n      __typename\n    }\n    geography {\n      lbsId\n      gaiaId\n      location {\n        latitude\n        longitude\n        __typename\n      }\n      isGeocoded\n      shouldShowMapCentralPin\n      __typename\n    }\n    propertyRedirectUrl\n    ...DestinationBreadcrumbsSearchResult\n    ...DestinationMessageSearchResult\n    ...FilterCountsSearchRequestResult\n    ...HitCollectionSearchResult\n    ...ADLSearchResult\n    ...MapSearchResult\n    ...ExpandedGroupsSearchResult\n    ...PagerSearchResult\n    ...SearchTermCarouselSearchResult\n    ...InternalToolsSearchResult\n    ...SEOMetaDataParamsSearchResult\n    ...GlobalInlineMessageSearchResult @include(if: $vrbo_web_global_messaging_alert)\n    ...GlobalBannerContainerSearchResult @include(if: $vrbo_web_global_messaging_banner)\n    __typename\n  }\n  ...RequestMarkerFragment\n}\n\nfragment DestinationBreadcrumbsSearchResult on SearchResult {\n  destination {\n    breadcrumbs {\n      name\n      url\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HitCollectionSearchResult on SearchResult {\n  page\n  pageSize\n  listings {\n    ...HitListing\n    __typename\n  }\n  pinnedListing {\n    listing {\n      availabilityInfo {\n        status\n        __typename\n      }\n      ...HitListing\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HitListing on Listing {\n  virtualTourBadge {\n    name\n    id\n    helpText\n    __typename\n  }\n  amenitiesBadges {\n    name\n    id\n    helpText\n    __typename\n  }\n  multiUnitProperty\n  images {\n    altText\n    c6_uri\n    c9_uri\n    __typename\n  }\n  listingNamespace\n  ...HitInfoListing\n  __typename\n}\n\nfragment HitInfoListing on Listing {\n  ...DetailsListing\n  ...PriceListing\n  ...RatingListing\n  ...GeoDistanceListing\n  detailPageUrl\n  instantBookable\n  minStayRange {\n    minStayHigh\n    minStayLow\n    __typename\n  }\n  listingId\n  rankedBadges(rankingStrategy: SERP) {\n    id\n    helpText\n    name\n    __typename\n  }\n  propertyId\n  listingNumber\n  propertyType\n  propertyMetadata {\n    headline\n    propertyName\n    __typename\n  }\n  superlativesBadges: rankedBadges(rankingStrategy: SERP_SUPERLATIVES) {\n    id\n    helpText\n    name\n    __typename\n  }\n  unitMessage(assetVersion: 1) {\n    iconText {\n      message\n      icon\n      messageValueType\n      __typename\n    }\n    __typename\n  }\n  unitMetadata {\n    unitName\n    __typename\n  }\n  __typename\n}\n\nfragment DetailsListing on Listing {\n  bathrooms {\n    full\n    half\n    toiletOnly\n    __typename\n  }\n  bedrooms\n  propertyType\n  sleeps\n  petsAllowed\n  spaces {\n    spacesSummary {\n      area {\n        areaValue\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PriceListing on Listing {\n  priceSummary: priceSummary {\n    priceTypeId\n    edapEventJson\n    formattedAmount\n    roundedFormattedAmount\n    pricePeriodDescription\n    priceAccurate\n    __typename\n  }\n  priceSummarySecondary: priceSummary(summary: \"displayPriceSecondary\") {\n    priceTypeId\n    edapEventJson\n    formattedAmount\n    roundedFormattedAmount\n    pricePeriodDescription\n    __typename\n  }\n  priceLabel: priceSummary(summary: \"priceLabel\") {\n    priceTypeId\n    pricePeriodDescription\n    __typename\n  }\n  __typename\n}\n\nfragment RatingListing on Listing {\n  averageRating\n  reviewCount\n  __typename\n}\n\nfragment GeoDistanceListing on Listing {\n  geoDistance {\n    text\n    relationType\n    __typename\n  }\n  __typename\n}\n\nfragment ExpandedGroupsSearchResult on SearchResult {\n  expandedGroups {\n    ...ExpandedGroupExpandedGroup\n    __typename\n  }\n  __typename\n}\n\nfragment ExpandedGroupExpandedGroup on ExpandedGroup {\n  listings {\n    ...HitListing\n    ...MapHitListing\n    __typename\n  }\n  mapViewport {\n    neLat\n    neLong\n    swLat\n    swLong\n    __typename\n  }\n  __typename\n}\n\nfragment MapHitListing on Listing {\n  ...HitListing\n  geoCode {\n    latitude\n    longitude\n    __typename\n  }\n  __typename\n}\n\nfragment FilterCountsSearchRequestResult on SearchResult {\n  id\n  resultCount\n  filterGroups {\n    groupInfo {\n      name\n      id\n      __typename\n    }\n    filters {\n      count @include(if: $filterCounts)\n      checked\n      filter {\n        id\n        name\n        refineByQueryArgument\n        description\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MapSearchResult on SearchResult {\n  mapViewport {\n    neLat\n    neLong\n    swLat\n    swLong\n    __typename\n  }\n  page\n  pageSize\n  listings {\n    ...MapHitListing\n    __typename\n  }\n  pinnedListing {\n    listing {\n      ...MapHitListing\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PagerSearchResult on SearchResult {\n  fromRecord\n  toRecord\n  pageSize\n  pageCount\n  page\n  resultCount\n  __typename\n}\n\nfragment DestinationMessageSearchResult on SearchResult {\n  destinationMessage(assetVersion: 4) {\n    iconTitleText {\n      title\n      message\n      icon\n      messageValueType\n      link {\n        linkText\n        linkHref\n        __typename\n      }\n      __typename\n    }\n    iconText {\n      message\n      icon\n      messageValueType\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ADLSearchResult on SearchResult {\n  parsedParams {\n    q\n    coreFilters {\n      adults\n      children\n      pets\n      minBedrooms\n      maxBedrooms\n      minBathrooms\n      maxBathrooms\n      minPrice\n      maxPrice\n      minSleeps\n      __typename\n    }\n    dates {\n      arrivalDate\n      departureDate\n      __typename\n    }\n    sort\n    __typename\n  }\n  page\n  pageSize\n  pageCount\n  resultCount\n  fromRecord\n  toRecord\n  pinnedListing {\n    listing {\n      listingId\n      __typename\n    }\n    __typename\n  }\n  listings {\n    listingId\n    __typename\n  }\n  filterGroups {\n    filters {\n      checked\n      filter {\n        groupId\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  geography {\n    lbsId\n    name\n    description\n    location {\n      latitude\n      longitude\n      __typename\n    }\n    primaryGeoType\n    breadcrumbs {\n      name\n      countryCode\n      location {\n        latitude\n        longitude\n        __typename\n      }\n      primaryGeoType\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RequestMarkerFragment on Query {\n  requestmarker\n  __typename\n}\n\nfragment SearchTermCarouselSearchResult on SearchResult {\n  discoveryXploreFeeds {\n    results {\n      id\n      title\n      items {\n        ... on SearchDiscoveryFeedItem {\n          type\n          imageHref\n          place {\n            uuid\n            name {\n              full\n              simple\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  typeaheadSuggestion {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InternalToolsSearchResult on SearchResult {\n  internalTools {\n    searchServiceUrl\n    __typename\n  }\n  __typename\n}\n\nfragment SEOMetaDataParamsSearchResult on SearchResult {\n  page\n  resultCount\n  pageSize\n  geography {\n    name\n    lbsId\n    breadcrumbs {\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalInlineMessageSearchResult on SearchResult {\n  globalMessages {\n    ...GlobalInlineAlertGlobalMessages\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalInlineAlertGlobalMessages on GlobalMessages {\n  alert {\n    action {\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    body {\n      text {\n        value\n        __typename\n      }\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    severity\n    title {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalBannerContainerSearchResult on SearchResult {\n  globalMessages {\n    ...GlobalBannerGlobalMessages\n    __typename\n  }\n  __typename\n}\n\nfragment GlobalBannerGlobalMessages on GlobalMessages {\n  banner {\n    body {\n      text {\n        value\n        __typename\n      }\n      link {\n        href\n        text {\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    id\n    severity\n    title {\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        return scrapy.http.JsonRequest(
            "https://www.vrbo.com/serp/g",
            callback=self.begin_parse, data=data)

        pass

    def listing_parse(self, response, detail=True):
        try:
            listings = [x for x in json.loads(response.body)['data']['results']['listings']]
        except TypeError:
            with open('TypeErrorListingResponse.txt', 'wb+') as file:
                file.write(response.request._body)
            raise

        if not detail:
            for lstng in listings:
                page = ListingDictParser.ListingDictParser(lstng)
                listing = items.Listing()
                listing['unit_id'] = page.unit_id()
                listing['title'] = page.title()
                listing['property_type'] = page.property_type()
                listing['bedrooms'] = page.bedrooms()
                listing['bathrooms'] = page.bathrooms()
                listing['sleeps'] = page.sleeps()
                listing['area_value'] = page.area_value()
                listing['rating'] = page.rating()
                listing['am_reviews'] = page.am_reviews()
                listing['page_url'] = page.page_url()
                listing['all_photo_url'] = page.all_photo_url()
                try:
                    listing['price'] = page.price()
                except TypeError:
                    listing['price'] = None
                listing['latitude'] = page.latitude()
                listing['longitude'] = page.longitude()
                yield listing
            pass
        else:
            for lstng in listings:
                page = ListingDictParser.ListingDictParser(lstng)
                yield scrapy.Request('https://www.vrbo.com' + page.page_url(), callback=self.detail_page_parse)

    def detail_page_parse(self, response):
        page = DetailPageDictParser.DetailPageDictParser(response)
        listing = items.DetailPage()

        listing['unit_id'] = page.unit_id()
        listing['title'] = page.title()
        listing['property_type'] = page.property_type()
        listing['bedrooms'] = page.bedrooms()
        listing['bathrooms'] = page.bathrooms()
        listing['sleeps'] = page.sleeps()
        listing['area_value'] = page.area_value()
        listing['area_units'] = page.area_units()
        listing['rating'] = page.rating()
        listing['am_reviews'] = page.am_reviews()
        listing['page_url'] = page.page_url()
        listing['address_city'] = page.address_city()
        listing['address_country'] = page.address_country()
        listing['postal_code'] = page.postal_code()
        listing['state_province'] = page.state_province()
        listing['all_photo_url'] = page.all_photo_url()
        listing['features'] = page.features()
        listing['price_amount'] = page.price_amount()
        listing['price_currency'] = page.price_currency()
        listing['latitude'] = page.latitude()
        listing['longitude'] = page.longitude()
        listing['availability_begin'] = page.availability_begin()
        listing['availability_end'] = page.availability_end()
        listing['availability_min_stay_default'] = page.availability_min_stay_default()
        listing['availability_string'] = page.availability_string()
        yield listing

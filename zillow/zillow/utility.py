from urllib import parse
import json
import urllib.parse


def create_search_link_meta(place, min_price=None, max_price=None, min_lot_size=None, max_lot_size=None, page_num=None):
    # home_type // house // mobile // condo // multifamily // apartment // land // townhouse
    if min_lot_size is not None and max_lot_size is not None:
        lot_string = ', "lot":{"max":' + str(max_lot_size) + ',"min":' + str(min_lot_size) + '}'
    elif min_lot_size is not None and max_lot_size is None:
        lot_string = ', "lot":{"min":' + str(min_lot_size) + '}'
    elif max_lot_size is not None and min_lot_size is None:
        lot_string = ', "lot":{"max":' + str(max_lot_size) + '}'
    else:
        lot_string = ''

    if min_price is not None and max_price is not None:
        price_string = ', "price":{"max":' + str(max_price) + ',"min":' + str(min_price) + '}'
    elif min_price is not None and max_price is None:
        price_string = ', "price":{"min":' + str(min_price) + '}'
    elif max_price is not None and min_price is None:
        price_string = ', "price":{"max":' + str(max_price) + '}'
    else:
        price_string = ''
    if page_num is not None and page_num != 1:
        page_num_str_1 = f'{page_num}_p/'
        page_num_str_2 = f'"currentPage":{page_num}'
    else:
        page_num_str_1 = ''
        page_num_str_2 = ''

    if place == "Puerto Rico":
        start = "https://www.zillow.com/pr/sold/_type/"+page_num_str_1+"?searchQueryState="
        query_str = '{"pagination":{'+page_num_str_2+'},"usersSearchTerm":"Puerto Rico","mapBounds":{"west":-69.13794728906248,"east":-64.02930471093748,"south":16.090167116588336,"north":20.28488306530533},"regionSelection":[{"regionId":48,"regionType":2}],"isMapVisible":true,"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"fore":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"pmf":{"value":false},"pf":{"value":false},"rs":{"value":true}' + price_string + ',"mp":{"min":0,"max":99999}' + lot_string + '},"isListVisible":true,"mapZoom":8}'
    elif place == "Texas":
        start = "https://www.zillow.com/tx/sold/_type/"+page_num_str_1+"?searchQueryState="
        query_str = '{"pagination":{'+page_num_str_2+'},"usersSearchTerm":"TX","mapBounds":{"west":-110.29412665625,"east":-89.85955634375,"south":23.487216521664003,"north":38.551419223891386},"regionSelection":[{"regionId":54,"regionType":2}],"isMapVisible":true,"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"fore":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"pmf":{"value":false},"pf":{"value":false},"rs":{"value":true}' + price_string + ',"mp":{"min":0,"max":99999}' + lot_string + '},"isListVisible":true,"mapZoom":8}'
    else:
        raise Exception("Place do not exist")
    url = start + urllib.parse.quote(query_str)
    meta = {"place": place,
            'min_price': min_price,
            'max_price': max_price,
            'min_lot_size': min_lot_size,
            'max_lot_size': max_lot_size,
            'page_num': page_num}
    return url, meta


if __name__ == '__main__':
    print(create_search_link_meta("Puerto Rico"))
    print(create_search_link_meta("Puerto Rico", 10000))
    print(create_search_link_meta("Puerto Rico", min_price=10000, max_price=100000))
    print(create_search_link_meta("Puerto Rico", min_lot_size=8000))
    print(create_search_link_meta("Puerto Rico"))
    print(create_search_link_meta("Puerto Rico", min_price=100000, max_price=1000000, min_lot_size=1000,
                                  max_lot_size=10000))

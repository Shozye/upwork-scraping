from police_calls.functions import *


def main():
    initialize_directories()
    """
    Uncomment one of the following functions
    """
    # scrape()
    # parse()
    scrape_date('07', '2020') # month and year as strings.


if __name__ == '__main__':
    main()

class ListingPage:
    def __init__(self, browser, url):
        self.browser = browser
        self.browser.get(url)
        more_description = "span[more-label=''][_ngcontent-c27='']"

    def gather_data(self):
        data = dict()
        data["thumb_photo"] = self.get_thumb_photo()
        data["url"] = self.get_url()
        data["name"] = self.get_name()
        data["title"] = self.get_title()
        data["HQ_location"] = self.get_HQ_location()
        data["website"] = self.get_website()
        data["overview"] = self.get_overview()
        data["team_members"] = self.get_team_members() # list with photo / name / position tuple
        data["locations"] = self.get_locations() # list of string with addresses industries dictionary string -> list  # "Health Care" -> [Health Care Services]
        data["transactions"] = self.get_transactions() # list with dictionaries with keys "date", "industry".May also contain logo of client company and middle company

    def get_transactions(self):
        pass

    def get_thumb_photo(self):
        pass

    def get_url(self):
        pass

    def get_name(self):
        pass

    def get_title(self):
        pass

    def get_HQ_location(self):
        pass

    def get_website(self):
        pass

    def get_overview(self):
        pass

    def get_team_members(self):
        pass

    def get_locations(self):
        pass

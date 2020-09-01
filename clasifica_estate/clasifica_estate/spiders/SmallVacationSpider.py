import scrapy

from .. import items
from .. import utility_func


class SmallVacationSpider(scrapy.Spider):
    name = 'vacSpider'
    def start_requests(self):
        url = 'https://www.clasificadosonline.com/UDVacListing.asp?VacCat=%25&Area=%25&Submit=Search%2FBusqueda&Keyword='
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css("td[height='50'][valign='middle'] a"):
            yield response.follow(a, callback=self.parse)
        for a in response.css("span.Ver11C a"):
            yield response.follow(a, callback=self.announcement_parse)
        pass

    def announcement_parse(self, response):
        announcement = items.VacRentalAnnouncement()
        announcement["vacation_id"] = response.url.split("=")[1]
        announcement["title"] = response.css("td.translate b::text").get()
        base_info = response.css("td.translate.Ver12C p")[1].css("::text").getall()
        announcement["category"] = utility_func.strip2(base_info[0]).split(": ")[1][:-1]
        announcement["city"] = utility_func.strip2(base_info[1]).split(": ")[1]
        announcement["rate_night"] = utility_func.strip2(utility_func.strip2(base_info[2]).split(": ")[1])
        announcement["amount_of_rooms"] = response.css("span.Tahoma14::text").getall()[0].split(": ")[1][:-1]
        announcement["phone1"] = response.css("span.Tahoma14::text").getall()[1]
        if len(response.css("span.Tahoma14::text").getall()) == 3:
            announcement["phone2"] = response.css("span.Tahoma14::text").getall()[2]
        else:
            announcement["phone2"] = None
        announcement["website_url"] = response.css("a.Ver12nounder[target='_blank']::text").get()
        if not announcement["website_url"].startswith('www') and not announcement["website_url"].startswith("https"):
            announcement["website_url"] = None
        announcement["photo_urls"] = response.css("div.MagicScroll a").xpath("@href").getall()
        if len(announcement["photo_urls"]) == 0:
            announcement["photo_urls"] = [response.css("#Trans").xpath("@href").get()]
        if announcement["photo_urls"] == [None]:
            announcement["photo_urls"] = None
        announcement["description"] = response.css("span.Tah12nounder::text").get()
        yield announcement

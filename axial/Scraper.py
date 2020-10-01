from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .ListingPage import ListingPage
import json

path = r"C:\Users\Rodzice.Mateusz-PC\Desktop\PythonProjects\BenHaynorScraping\axial\chromedriver.exe"
driver = webdriver.Chrome(path)


def gather_links(browser):
    urls = []
    for page in range(1, 83):
        browser.get(f"https://www.axial.net/forum/companies/united-states-business-brokers/{page}/")
        elems = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.teaser1-wrap")))
        links = [elem.get_attribute('href') for elem in elems]
        urls.extend(links)
        print(page, f"found {len(links)}")
    with open("urls.json", 'w+') as file:
        file.write(json.dumps(urls, indent=4))


def get_data(browser):
    with open("urls.json") as file:
        urls = json.loads(file.read())
    data = []
    for url in urls:
        listing_page = ListingPage(browser, url)
        data.extend(listing_page.gather_data())

        with open("data.json") as file:
            file.write(json.dumps(data))


if __name__ == "__main__":
    gather_links(driver)

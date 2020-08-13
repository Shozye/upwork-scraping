from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup



class Scraper:
    """
    Class created to help manage scraping from website
    """
    def __init__(self):
        self.counter = 1 # used to save innerhtmls
        self.path = r'C:\Users\Rodzice.Mateusz-PC\Desktop\PythonProjects\BenHaynorScraping\chromedriver.exe'
        self.browser = webdriver.Chrome(self.path)
        self.search_url = 'https://webapp3.sanantonio.gov/policecalls/Reports.aspx'

    def go_to_search_site(self):
        self.browser.get(self.search_url)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'btnSearch')))

    def enter_date(self, start_date):
        """
        method that enters date to search criteria
        :param start_date: string formatted mm/01/yyyy
        """
        start_data_form = self.browser.find_element_by_name('txtStart')
        start_data_form.send_keys(start_date)
        disabler_focus = self.browser.find_element_by_css_selector('p strong')
        disabler_focus.click()

        month_button = self.browser.find_element_by_id('rdbSearchRange_2')
        month_button.click()

    def select_dropdown_menu(self, value, value2):
        select_menu = self.browser.find_element_by_id('ddlCategory')
        select = Select(select_menu)
        select.select_by_value(value)

        if value2 is not None:
            select2_menu = self.browser.find_element_by_id('ddlCouncilDistrict')
            select2 = Select(select2_menu)
            select2.select_by_value(value2)

    def click_search(self):
        button = self.browser.find_element_by_id('btnSearch')
        button.click()
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, 'lblMessage')))

    def has_exceeded(self):
        """
        Checks if amount of data exceeds limit of 10000
        :return: boolean
        """
        span = self.browser.find_element_by_id('lblMessage')
        if span.text[:6] == '10,000':
            return True
        else:
            return False

    def search(self, start_data, value, value2):
        self.go_to_search_site()
        self.enter_date(start_data)
        self.select_dropdown_menu(value, value2)
        self.click_search()

    def save(self):
        table = self.browser.find_element_by_css_selector('table#gvCFS tbody')
        with open(f'innerhtmls/{str(self.counter)}', 'w+') as file:
            file.write(table.get_attribute('innerHTML'))
            self.counter += 1

    def format_table(self):
        """
        Method that should be use at result site
        :return: list with all rows
        """
        nullized_data = []
        table = self.browser.find_element_by_css_selector('table#gvCFS tbody')
        text = table.get_attribute('innerHTML')
        soup = BeautifulSoup(text, features="html.parser")
        trs = soup.find_all('tr')[1:]
        for record in trs:
            record_data = list(map(lambda x: x.text, record.find_all('td')))
            nullized_record_data = ['' if x == '\xa0' else x for x in record_data]
            nullized_data.append(nullized_record_data)
        return nullized_data








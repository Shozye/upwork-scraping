from bs4 import BeautifulSoup
import csv
from police_calls.scraper import Scraper
from police_calls.utility import *
import os


def scrape():
    """
    This function is used to scrape all data from website and download it to txt files in innerhtmls directory
    This data is innerHTML of table
    range of searching is everything in start_date_list() specified in utility.py
    :return:
    """
    date_lst = start_date_list()
    drop_down_lst = dropdown_list()
    council_nums = council_districts()

    a = Scraper()
    for date in date_lst:
        for drop_down in drop_down_lst:
            a.search(date, drop_down, None)
            if a.has_exceeded():
                for council_num in council_nums:
                    a.search(date, drop_down, council_num)
                    if a.has_exceeded():
                        print(date, drop_down, council_num)
                    else:
                        a.save()
            else:
                a.save()


def scrape_date(month, year):
    """
    :param month: string format mm
    :param year: string format yyyy
    scrape data from specified month and year and appends to data.csv
    """
    rows = []
    date = f'{month}/01/{year}'
    drop_down_lst = dropdown_list()
    council_nums = council_districts()
    a = Scraper()
    for drop_down in drop_down_lst:
        a.search(date, drop_down, None)
        if a.has_exceeded():
            for council_num in council_nums:
                a.search(date, drop_down, council_num)
                if a.has_exceeded():
                    print(date, drop_down, council_num)
                else:
                    rows.extend(a.format_table())
        else:
            rows.extend(a.format_table())
    if os.path.isfile('data.csv'):
        with open('data.csv', 'a', newline ='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    with open(f'scrape{month}{year}.csv', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers())
        writer.writerows(rows)


def parse():
    """
    Takes every file in innerhtmls directory and parses innerhtml data inside.
    Creates csv rows and writes everything to data.csv
    Function creates new file every time it is run.
    """
    AMOUNT = 4160
    path = r'C:\Users\Rodzice.Mateusz-PC\Desktop\PythonProjects\BenHaynorScraping\innerhtmls'
    with open('data.csv', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        headers = csv_headers()
        writer.writerow(headers)
        for i in range(1, AMOUNT + 1):
            if i % 100 == 0:
                print(f"{i}-th file done")
            filename = path + '/' + str(i)
            with open(filename) as file:
                a = file.read()
            soup = BeautifulSoup(a, features="html.parser")
            trs = soup.find_all('tr')[1:]
            for record in trs:
                record_data = list(map(lambda x: x.text, record.find_all('td')))
                nullized_record_data = ['' if x == '\xa0' else x for x in record_data]
                writer.writerow(nullized_record_data)

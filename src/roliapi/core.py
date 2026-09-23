import json
import requests
import cloudscraper
from bs4 import BeautifulSoup

class roliapi:
    def __init__(self, item_details: dict = None):
        if item_details == None:
            self.update_data()
    
    def get_item_data(self, item_id: int):
        item_obj = self.item_details["items"][str(item_id)]
        
        return Item(item_id, item_obj[0], item_obj[1], item_obj[2], item_obj[3], item_obj[4])

    def update_data(self):
        scraper = cloudscraper.create_scraper()
        self.item_details = scraper.get("https://rolimons.com/itemapi/itemdetails").json()
        if not self.item_details["success"]:
            pass # Add proper error handling       
class Item:
    def __init__(self, id, name, acronym, rap, value, default_value, best_price = None, picture = None):
        self.id = id # key
        self.name = name # index 0
        self.acronym = acronym # index 1
        self.rap = rap # index 2
        self.value = value # index 3
        self.default_value = default_value # index 4
        self.best_price = best_price # requires webscraping
        self.picture = picture # dunno yet

    def get_best_price(self):
        BASE_URL = "https://rolimons.com/item/"

        scraper = cloudscraper.create_scraper()
        url = BASE_URL + str(self.id)
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        best_price = soup.select_one("div.d-flex.value-stat-box.bg-primary > div:not([class]) .value-stat-data")
        self.best_price = int(best_price.text.replace(',', ''))

    def get_item_picture(self):
        BASE_URL = "https://rolimons.com/item/"

        scraper = cloudscraper.create_scraper()
        url = BASE_URL + str(self.id)
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        img = soup.find('img', class_=['img-responsive', 'img-fluid', 'rounded', 'm-3', 'shadow-sm'])
        img_src = img.get('src')
        self.picture = img_src


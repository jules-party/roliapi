import json
import cloudscraper

class RolimonData:
    def __init__(self, item_details: dict = None):
        if item_details == None:
            self.update_data()
    
    def get_item_data(self, item_id: int):
        item_dict = self.item_details.get("items", {})
        item_obj = item_dict.get(str(item_id))
        
        return Item(item_id, item_obj[0], item_obj[1], item_obj[2], item_obj[3], item_obj[4])

    def update_data(self):
        scraper = cloudscraper.create_scraper()
        self.item_details = scraper.get("https://rolimons.com/itemapi/itemdetails").json()
        if not self.item_details.get("success"):
            raise NotImplementedError # Add proper error handling       
class Item:
    def __init__(self, id, name, acronym, rap, value, default_value, best_price = None, picture = None):
        self.id = id # key
        self.name = name # index 0
        self.acronym = acronym # index 1
        self.rap = rap # index 2
        self.value = value # index 3
        self.default_value = default_value # index 4

    def get_best_price(self, roblo_security):
        BASE_URL = f"https://catalog.roblox.com/v1/catalog/items/{self.id}/details"

        scraper = cloudscraper.create_scraper()
        scraper.cookies[".ROBLOSECURITY"] = roblo_security

        response = scraper.get(BASE_URL, params={"itemType": "Asset"})
        response.raise_for_status()
        data = response.json()

        lowest = data.get("lowestResalePrice")
        return lowest

    def get_item_picture(self, roblo_security):
        BASE_URL = "https://thumbnails.roblox.com/v1/assets"

        scraper = cloudscraper.create_scraper()
        scraper.cookies[".ROBLOSECURITY"] = roblo_security

        response = scraper.get(BASE_URL, params={
            "assetIds": self.id,
            "size": "420x420",
            "format": "Png",
            "isCircular": "false"
        })

        response.raise_for_status()
        data = response.json()

        entries = data.get("data", [])
        if not entries:
            return None

        entry = entries[0]
        if entry.get("state") != "Completed":
            return None

        picture = entry.get("imageUrl")
        return picture

import cloudscraper


class Item:
    def __init__(self, id, name, acronym, rap, value, default_value, best_price = None, picture = None):
        self.id: int = id # key
        self.name: str = name # index 0
        self.acronym: str = acronym # index 1
        self.rap: int = rap # index 2
        self.value: int = value # index 3
        self.default_value: int  = default_value # index 4
        self.lowest_price: int | None = None # Must be set, to save on API
        self.image_url: str | None = None # Same as before, must be set using get_item_picture()

    def get_best_price(self, roblo_security) -> int:
        BASE_URL = f"https://catalog.roblox.com/v1/catalog/items/{self.id}/details"

        scraper = cloudscraper.create_scraper()
        scraper.cookies[".ROBLOSECURITY"] = roblo_security

        response = scraper.get(BASE_URL, params={"itemType": "Asset"})
        response.raise_for_status()
        data = response.json()

        lowest = data.get("lowestResalePrice")
        return lowest

    def get_item_picture(self, roblo_security) -> str:
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

class RolimonData:
    def __init__(self, item_details: dict | None = None):
        if item_details == None:
            self.update_data()

    # Rolimon has missing data for newer-ish items, so just fallback to Roblox API for general info
    # Though we miss out on item value (even if its on the Rolimon website)
    # We could scrape the item's page for Value using BS4, but I'd rather stray away from WebScraping
    def _roblox_fallback(self, item_id: int, roblo_security: str) -> Item:
        BASE_URL = f"https://catalog.roblox.com/v1/catalog/items/{item_id}/details"

        scraper = cloudscraper.create_scraper()
        scraper.cookies[".ROBLOSECURITY"] = roblo_security

        response = scraper.get(BASE_URL, params={"itemType": "Asset"})
        response.raise_for_status()
        details = response.json()

        name = details.get("name")

        collectible_id = details.get("collectibleItemId")
        rap = None
        if collectible_id:
            rap_url = f"https://apis.roblox.com/marketplace-sales/v1/item/{collectible_id}/resale-data"
            rap_res = scraper.get(rap_url)
            if rap_res.status_code == 200:
                rap = rap_res.json().get("recentAveragePrice")
                rap = int(rap)

        item = Item(item_id, name, None, rap if rap is not None else -1, -1, -1)
        return item

    def get_item_data(self, item_id: int, roblo_security: str = None) -> Item:
        item_dict = self.item_details.get("items", {})
        item_obj = item_dict.get(str(item_id))

        if not item_obj:
            item = self._roblox_fallback(item_id, roblo_security)
            return item
        
        return Item(item_id, item_obj[0], item_obj[1], item_obj[2], item_obj[3], item_obj[4])


    def get_all_items(self) -> list[Item]:
        items_raw = self.item_details.get("items")
        items = []
        for item_id in items_raw:
            items.append(self.get_item_data(item_id))

        return items


    def update_data(self) -> None:
        scraper = cloudscraper.create_scraper()
        self.item_details = scraper.get("https://rolimons.com/itemapi/itemdetails").json()
        if not self.item_details.get("success"):
            raise NotImplementedError # Add proper error handling   
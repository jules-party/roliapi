import cloudscraper

class Item:
    def __init__(self, data: dict = {}):
        self.id: int = data.get("id")# key
        self.name: str = data.get("name") # index 0
        self.acronym: str = data.get("acronym") # index 1
        self.rap: int = data.get("rap") # index 2
        self.value: int = data.get("value") # index 3
        self.default_value: int  = data.get("default_value") # index 4
        self.lowest_price: int = data.get("lowest_price") # Must be set, to save on API
        self.image_url: str = data.get("image_url") # Same as before, must be set using get_item_picture()

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
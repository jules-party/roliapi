import cloudscraper

class Player:
    def __init__(self, data: dict = {}):
        self.id: int = data.get("id")
        self.name: str = data.get("name")
        self.online: bool = data.get("online")
        self.value: int = data.get("value")
        self.rap: int = data.get("rap")
        self.premium: bool = data.get("premium")
        self.inventory: dict = data.get("inventory")
        self.item_holds: list[int] = data.get("holds")
        self.avatar_url: str = data.get("avatar_url")

    def get_player_avatar(self):
        url="https://thumbnails.roblox.com/v1/users/avatar"
        params = {
            "userIds": self.id,
            "size": "420x420",
            "format": "Png",
            "isCircular": False
        }

        scraper = cloudscraper.create_scraper()
        res = scraper.get(url, params=params)
        data = res.json().get("data")

        image_url = data[0].get("imageUrl")

        return image_url
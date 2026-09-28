import cloudscraper

from .endpoints.items import Item
from .endpoints.player import Player

class RolimonData:
    def __init__(self, item_details: dict = None):
        if item_details == None:
            self.update_data()

    def update_data(self) -> None:
        scraper = cloudscraper.create_scraper()
        self.item_details = scraper.get("https://api.rolimons.com/items/v3/itemdetails").json()
        if not self.item_details.get("success"):
            raise NotImplementedError # Add proper error handling

    def get_item_data(self, item_id: int) -> Item:
        item_dict = self.item_details.get("assets", {})
        item_obj = item_dict.get(str(item_id))
        
        return Item({
            'id': item_id,
            'name': item_obj[0],
            'acronym': item_obj[1],
            'rap': item_obj[2],
            'value': item_obj[3],
            'default_value': item_obj[4]
        })

    def get_all_items(self) -> list[Item]:
        items_raw = self.item_details.get("assets")
        items = []
        for item_id in items_raw:
            items.append(self.get_item_data(item_id))

        return items

    def get_player_data(self, player_id: int) -> Player:
        info_url = f"https://api.rolimons.com/players/v1/playerinfo/{player_id}"
        assets_url = f"https://api.rolimons.com/players/v1/playerassets/{player_id}"

        scraper = cloudscraper.create_scraper()
        info_res = scraper.get(info_res)
        assets_res = scraper.get(assets_url)

        player_info = info_res.json()
        player_assets = assets_res.json()

        return Player({
            'id': player_id,
            'name': player_info.get("name"),
            'online': player_assets.get("isOnline"),
            'value': player_info.get("value"),
            'rap': player_info.get("rap"),
            'premium': player_info.get("premium"),
            'inventory': player_assets.get("playerAssets"),
            'holds': player_assets.get("holds")
        })
class Player:
    def __init__(self, data: dict = {}):
        self.id: int = data.get("id")
        self.name: str = data.get("name")
        self.value: int = data.get("value")
        self.rap: int = data.get("rap")
        self.premium: bool = data.get("premium")
        self.inventory: dict = data.get("inventory")
        self.item_holds: list[int] = data.get("holds")
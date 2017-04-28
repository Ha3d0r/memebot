from bs4 import BeautifulSoup
from enum import Enum

class TankClass(Enum):
    """Represents the class of a tank"""
    LT = "LT"
    MT = "MT"
    HT = "HT"
    TD = "TD"
    SPG = "SPG"

    def create(cell):
        """Gets the type of a tank"""
        span = cell.find("span")
        title = span.get("title")
        if title == "Medium tank":
            return TankClass.MT
        elif title == "Tank destroyer":
            return TankClass.TD
        elif title == "Light tank":
            return TankClass.LT
        elif title == "Heavy tank":
            return TankClass.HT
        elif title == "SPG":
            return TankClass.SPG

class Tank:
    """Represents a tank of a player"""
    tank_class: TankClass
    tier: int
    battles: int
    damage: float
    winrate: float
    wn8: float

    def __init__(self, row):
        cells = row.find_all("td")
        
        self.tanktype = TankClass.create(cells[4])
        self.tier = int(cells[6].get_text())
        self.battles = int(cells[9].get_text())
        self.damage = float(cells[7].get_text().replace(',', '.'))
        self.winrate = float(cells[10].get_text().replace('%', '').replace(',', '.'))
        self.wn8 = float(cells[11].get_text().replace(',', '.'))

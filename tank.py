from bs4 import BeautifulSoup
from enum import Enum
from utils import comma_float, parse_percentage

class TankClass(Enum):
    """Represents the class of a tank"""
    LT = "Light tank"
    MT = "Medium tank"
    HT = "Heavy tank"
    TD = "Tank destroyer"
    SPG = "SPG"

    def create(cell):
        """Gets the type of a tank"""
        span = cell.find("span")
        title = span.get("title")

        return TankClass(title)

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
        self.damage = comma_float(cells[7].get_text())
        self.winrate = parse_percentage(cells[10].get_text())
        self.wn8 = comma_float(cells[11].get_text())

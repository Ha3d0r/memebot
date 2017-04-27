from enum import Enum
from bs4 import BeautifulSoup
from functools import reduce

class TankType(Enum):
    LT = "LT"
    MT = "MT"
    HT = "HT"
    TD = "TD"
    ARTA = "SPG"
    NONE = "none"

class Tank:
    tanktype: TankType
    tier: int
    battles: int
    wn8: float

    def __init__(self, row):
        """Parses a tank row into a tuple of (type, tier, battles, wn8)"""
        cells = row.find_all("td")
        type_cell = cells[4]
        tier_cell = cells[6]
        battles_cell = cells[9]
        wn8_cell = cells[11]

        self.tanktype = Tank.fetch_tanktype(type_cell)
        self.tier = int(tier_cell.get_text())
        self.battles = int(battles_cell.get_text())
        self.wn8 = float(wn8_cell.get_text().replace(',', '.'))

    def readable_tank(self):
        return "tier " + str(self.tier) + " " + str(self.tanktype) + ", " + str(self.battles) + " battles, " + str(self.wn8) + " wn8"

    def fetch_tanktype(cell):
        """Gets the type of a tank"""
        span = cell.find("span")
        title = span.get("title")
        if title == "Medium tank":
            return TankType.MT
        elif title == "Tank destroyer":
            return TankType.TD
        elif title == "Light tank":
            return TankType.LT
        elif title == "Heavy tank":
            return TankType.HT
        elif title == "SPG":
            return TankType.ARTA
        else:
            return TankType.NONE

class PlayerClassification:
    tanks: [Tank]
    avg_tier: float
    battles: int
    tank_types = {}
    error = None

    def __init__(self, soup):
        tanks_table = soup.find(id="tanks")

        if tanks_table is None:
            self.error = "User not found."
            return

        body = tanks_table.find("tbody")
        rows = body.find_all("tr")

        self.tanks = map(lambda x: Tank(x), rows)

        total_tier = 0
        self.battles = 0
        self.tank_types = {TankType.ARTA: 0, TankType.HT: 0, TankType.MT: 0, TankType.LT: 0, TankType.TD: 0}

        for tank in self.tanks:
            total_tier += tank.tier * tank.battles
            self.battles += tank.battles
            self.tank_types[tank.tanktype] += tank.battles

        if self.battles == 0:
            self.avg_tier = 0.0
        else:
            self.avg_tier = float(total_tier) / float(self.battles)

    def report(self):
        if self.error is not None:
            return self.error
        if self.battles == 0:
            return "This player has 0 battles, so I guess he's just an asshole ¯\_(ツ)_/¯"
        if self.avg_tier < 5.0:
            return "Filthy low tier sealclubber"
        else:
            most_played_type = max(self.tank_types, key=self.tank_types.get)
            if most_played_type == TankType.TD:
                return "Redline bush wanker"
            elif most_played_type == TankType.ARTA:
                return "Point & Click adventure gamer"
            elif most_played_type == TankType.HT:
                return "Braindead heavy driver"
            elif most_played_type == TankType.MT:
                return "Noob mediums, why u run away from fight"
            elif most_played_type == TankType.LT:
                return "Filthy light tank WN8 stetpedder"


def main():
    file = open("sample.html")
    soup = BeautifulSoup(file.read(), "html.parser")
    stats = PlayerClassification(soup)
    print(stats.report())

if __name__ == "__main__":
    main()

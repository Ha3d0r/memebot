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
    user: str

    def __init__(self, name, soup):
        self.user = name
        tanks_table = soup.find(id="tanks")

        if tanks_table is None:
            self.error = "User not found."
            return

        body = tanks_table.find("tbody")
        rows = body.find_all("tr")

        self.tanks = map(lambda x: Tank(x), rows)

        total_tier = 0
        self.battles = 0
        self.tiers = {key: 0 for key in range(1, 11)}
        self.tank_types = {TankType.HT: 0, TankType.MT: 0, TankType.LT: 0, TankType.TD: 0, TankType.ARTA: 0}

        for tank in self.tanks:
            total_tier += tank.tier * tank.battles
            self.battles += tank.battles
            self.tank_types[tank.tanktype] += tank.battles
            self.tiers[tank.tier] += tank.battles

        if self.battles == 0:
            self.avg_tier = 0.0
        else:
            self.avg_tier = float(total_tier) / float(self.battles)

    def classify(self):
        if self.error is not None:
            return self.error

    def percentage(lhs, rhs):
        return float(lhs) / float(rhs)

    def present(self):
        max_tier = self.tiers[max(self.tiers, key=self.tiers.get)]
        max_class = self.tank_types[max(self.tank_types, key=self.tank_types.get)]

        report = "Tiers:\n"
        for tier, battles in self.tiers.items():
            report += PlayerClassification.graph_bar(str(tier), PlayerClassification.percentage(battles, self.battles), PlayerClassification.percentage(max_tier, self.battles)) + "\n"
        
        report += "Tank types:\n"
        for tank_type, battles in self.tank_types.items():
            report += PlayerClassification.graph_bar(tank_type.value, PlayerClassification.percentage(battles, self.battles), PlayerClassification.percentage(max_class, self.battles)) + "\n"
        
        return report

    def graph_bar(title: str, percentage: float, max_percentage: float, colwidth = 5):
        padding = colwidth - len(title)
        return title + " " * padding + " |" + PlayerClassification.horizontal_bar(percentage, max_percentage, 40)
    
    def horizontal_bar(percentage: float, max_percentage: float, width: int = 40):
        filled = int(round((percentage / max_percentage) * float(width)))
        unfilled = 40 - filled
        return filled * "=" + unfilled * " " + " (" + str(round(percentage * 100, 2)) + "%)"

    def report(self):
        report = "**Results for player " + self.user + "**\n"
        if self.battles == 0:
            return "This player has 0 battles, so I guess he's just an asshole ¯\_(ツ)_/¯"

        report += "```" + self.present()

        report += "```\n:thinking: My verdict:\n"

        if self.avg_tier < 5.0:
            report += "Filthy low tier sealclubber"
        else:
            most_played_type = max(self.tank_types, key=self.tank_types.get)
            if most_played_type == TankType.TD:
                report += "Redline bush wanker"
            elif most_played_type == TankType.ARTA:
                report += "Point & Click adventure gamer"
            elif most_played_type == TankType.HT:
                report += "Braindead heavy driver"
            elif most_played_type == TankType.MT:
                report += "Noob mediums, why u run away from fight"
            elif most_played_type == TankType.LT:
                report += "Filthy light tank WN8 stetpedder"
        
        return report


def main():
    file = open("sample.html")
    soup = BeautifulSoup(file.read(), "html.parser")
    stats = PlayerClassification("apptux", soup)
    print(stats.report())

if __name__ == "__main__":
    main()

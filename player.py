from bs4 import BeautifulSoup
from enum import Enum
from utils import comma_float
from tank import Tank

class PeriodType(Enum):
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    OVERALL = ""

class PeriodStats:
    """Represents the statistics of a user over a certain period"""
    battles: int
    winrate: float
    wn8: float
    period: PeriodType

    def __init__(self, period: PeriodType, rows, column = 0):
        self.period = period
        self.battles = int(PeriodStats.get_col(rows[1], column))
        # we trim the '%' off the winrate, e.g. '54,38%' becomes '54,38'
        self.winrate = comma_float(PeriodStats.get_col(rows[3], column * 2 + 1).replace('%', ''))
        self.wn8 = comma_float(PeriodStats.get_col(rows[len(rows) - 1], column))

    @staticmethod
    def get_col(row, col = 0):
        """Gets the value of a specific row in the specified row of a HTML <tr>. """
        entries = row.find_all("td")
        return entries[col].get_text()

class Player:
    """Represents a Player in World of Tanks"""
    name: str
    tanks: [Tank]
    overall: PeriodStats
    day: PeriodStats
    week: PeriodStats
    month: PeriodStats

    # If any error is encountered while parsing
    # the player it is outputted in Player.error
    error: str = ""

    soup: BeautifulSoup

    def __init__(self, soup):
        self.soup = soup

        try:
            self.build_stats()
            self.build_tanks()

            self.name = self.get_real_name()
        except Exception:
            self.error += "User not found"

    def build_stats(self):
        """Builds overall and recent stats of this Player"""

        randoms_stat_tab = self.soup.find(id="tab1")

        table = randoms_stat_tab.find("table")
        rows = table.find_all("tr")

        self.overall = PeriodStats(PeriodType.OVERALL, rows)
        self.day = PeriodStats(PeriodType.DAY, rows, 1)
        self.week = PeriodStats(PeriodType.WEEK, rows, 2)
        self.month = PeriodStats(PeriodType.MONTH, rows, 3)

    def build_tanks(self):
        """Builds the list of played tanks by this Player"""

        tanks_table = self.soup.find(id="tanks")

        if tanks_table is None:
            self.error = "User not found"
            return

        body = tanks_table.find("tbody")
        rows = body.find_all("tr")

        self.tanks = map(lambda x: Tank(x), rows)

    def get_real_name(self):
        title_div = self.soup.find("div", id="title")
        header = title_div.find("h1")
        return header.get_text()

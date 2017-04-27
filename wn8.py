import urllib.request
from enum import Enum
from bs4 import BeautifulSoup

def read_stats(html):
    soup = BeautifulSoup(html, "html.parser")
    return PlayerStats(soup)

class RecentType(Enum):
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    OVERALL = ""

class PeriodStats:
    battles = ""
    winrate = ""
    wn8 = ""

    def __init__(self, rows, column = 0):
        self.battles = PeriodStats.get_col(rows[1], column)
        self.winrate = PeriodStats.get_col(rows[3], column * 2 + 1)
        self.wn8 = PeriodStats.get_col(rows[len(rows) - 1], column)

    def get_col(row, col = 0):
        """Gets the value of a specific row in the specified row of a HTML <tr>. """
        entries = row.find_all("td")
        return entries[col].get_text()

    def readable_stats(self):
        return "Battles: " + self.battles + "\nWinrate: " + self.winrate + "\nWN8: " + self.wn8

class PlayerStats:
    """A Class that contains a Player's stats"""

    error = None
    overall = None
    day = None
    week = None
    month = None

    def __init__(self, soup):
        randoms_stat_tab = soup.find(id="tab1")

        if randoms_stat_tab is None:
            self.error = "User not found"
            return

        table = randoms_stat_tab.find("table")
        rows = table.find_all("tr")

        self.overall = PeriodStats(rows)
        self.day = PeriodStats(rows, 1)
        self.week = PeriodStats(rows, 2)
        self.month = PeriodStats(rows, 3)
        
        self.name = self.get_real_name(soup)

    def readable_stats(self, recent_type: RecentType):
        if self.error is not None:
            return self.error
        
        period_stats = ("Overall stats", self.overall)

        if recent_type == RecentType.DAY:
            period_stats = ("24h stats", self.day)
        elif recent_type == RecentType.WEEK:
            period_stats = ("7d stats", self.week)
        elif recent_type == RecentType.MONTH:
            period_stats = ("30d stats", self.month)

        # use ```python``` code block so numbers get highlighted
        return "```python\n" + period_stats[0] + " of `" + self.name + "`:\n" + period_stats[1].readable_stats() + "```"

    def get_real_name(self, soup):
        title_div = soup.find("div", id="title")
        header = title_div.find("h1")
        return header.get_text()

def main():
    file = open("sample.html")
    stats = read_stats(file.read())
    print(stats.readable_stats(RecentType.OVERALL))

if __name__ == "__main__":
    main()

import urllib.request
from bs4 import BeautifulSoup

def fetch_wn8(name):
    with urllib.request.urlopen("https://wot-life.com/eu/player/" + name + "/") as response:
        html = response.read()

        return read_stats(html)
        
def read_stats(html):
    soup = BeautifulSoup(html, "html.parser")
    randoms_stat_tab = soup.find(id="tab1")
    
    if randoms_stat_tab is None:
        return "User not found"

    table = randoms_stat_tab.find("table")
    rows = table.find_all("tr")

    battles_row = rows[1]
    winrate_row = rows[3]
    wn8_row = rows[len(rows) - 1]
    
    battles = get_col(battles_row)
    winrate = get_col(winrate_row, 1)
    wn8 = get_col(wn8_row)
    
    name = get_real_name(soup)

    return name + " | " + wn8 + " WN8 | " + battles + " battles | " + winrate

def get_col(row, col = 0):
    entries = row.find_all("td")
    return entries[col].get_text()

def get_real_name(soup):
    title_div = soup.find("div", id="title")
    header = title_div.find("h1")
    return header.get_text()

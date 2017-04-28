from enum import Enum
from bs4 import BeautifulSoup
from player import Player, PeriodType

def read_stats(html, period):
    soup = BeautifulSoup(html, "html.parser")
    player = Player(soup)

    try:
        period = PeriodType(period)
    except ValueError:
        period = PeriodType.OVERALL

    return readable_stats(player, period)

def readable_stats(player: Player, period: PeriodType):
    if player.error != "":
        return player.error
    
    period_stats = ("[Overall] stats", player.overall)

    if period == PeriodType.DAY:
        period_stats = ("[24h] stats", player.day)
    elif period == PeriodType.WEEK:
        period_stats = ("[7d] stats", player.week)
    elif period == PeriodType.MONTH:
        period_stats = ("[30d] stats", player.month)

    periodic_stats = period_stats[1]

    # use ```python``` code block so numbers get highlighted
    return  ("```css\n"
            f"{period_stats[0]} for [{player.name}]:\n"
            f"Battles: {{{periodic_stats.battles}}}\n"
            f"Winrate: {{{periodic_stats.winrate}%}}\n"
            f"WN8: {{{periodic_stats.wn8}}}\n"
            "```")

def main():
    file = open("sample.html")
    print(read_stats(file.read(), "24h"))

if __name__ == "__main__":
    main()

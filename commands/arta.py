from bs4 import BeautifulSoup
from functools import reduce
from enum import Enum
from wotlife.player import Player
from wotlife.tank import Tank, TankClass

class Arta:
    player: Player
    username: str

    def __init__(self, player: Player, username: str):
        self.player = player
        self.username = username

        if player.error != "":
            return

    def report(self):
        if self.player.error != "":
            return f"Could not find {self.username} :fearful:"

        percentage = self.get_percentage() * 100.0
        rounded_percentage = round(percentage, 1)

        return f"{self.player.name} has played arta {rounded_percentage}% of the time. <:ebola:303821557631942656>"
    
    def get_percentage(self):
        if self.player.overall.battles == 0:
            return 0.0

        spg_battles = self.player.classes[TankClass.SPG]

        return (spg_battles / self.player.overall.battles)

def analyse_arta(html, username):
    soup = BeautifulSoup(html, "html.parser")
    player = Player(soup)
    stats = Arta(player, username)
    return stats.report()

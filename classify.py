from bs4 import BeautifulSoup
from functools import reduce
from enum import Enum
from player import Player
from tank import Tank, TankClass
from playerclassification import *

class PlayerClassification:
    player: Player
    username: str
    classifiers = []

    def __init__(self, player: Player, username: str):
        self.player = player
        self.username = username

        if player.error != "":
            return

        self.classifiers = all_classifiers()

    def report(self):
        if self.player.error != "":
            return f"Could not find {self.username} :fearful:"

        verdict = self.verdict()

        return (f":thinking: My verdict for {self.player.name}:\n"
                  f"```{verdict}```")
    
    def verdict(self):
        if self.player.overall.battles == 0:
            return "This player has 0 battles, so I guess he's just an asshole ¯\_(ツ)_/¯"

        for classifier in self.classifiers:
            match = classifier(self.player)
            if match.rate():
                return match.verdict()

        if self.player.overall.avg_tier < 5.0:
            return "Filthy low tier sealclubber"
        else:
            most_played_type = max(self.player.classes, key=self.player.classes.get)
            if most_played_type == TankClass.TD:
                return "Redline bush wanker"
            elif most_played_type == TankClass.SPG:
                return "Point & Click adventure gamer"
            elif most_played_type == TankClass.HT:
                return "Heavy driver"
            elif most_played_type == TankClass.MT:
                return "Noob mediums, why u run away from fight"
            elif most_played_type == TankClass.LT:
                return "Filthy light tank WN8 stetpedder"
def classify_player(html, username):
    soup = BeautifulSoup(html, "html.parser")
    player = Player(soup)
    stats = PlayerClassification(player, username)
    return stats.report()

def main():
    file = open("sample.html")
    print(classify_player(file.read()))

if __name__ == "__main__":
    main()

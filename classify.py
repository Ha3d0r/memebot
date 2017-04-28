from bs4 import BeautifulSoup
from functools import reduce
from enum import Enum
from player import Player
from tank import Tank, TankClass

class PlayerClassification:
    player: Player
    avg_tier: float
    tank_types = {}
    tiers = {}

    def __init__(self, player: Player):
        self.player = player

        if player.error != "":
            return

        total_tier = 0
        self.tiers = {key: 0 for key in range(1, 11)}
        self.tank_types = {TankClass.HT: 0, TankClass.MT: 0, TankClass.LT: 0, TankClass.TD: 0, TankClass.SPG: 0}

        if player.overall.battles > 0:
            for tank in player.tanks:
                total_tier += tank.tier * tank.battles
                self.tank_types[tank.tanktype] += tank.battles
                self.tiers[tank.tier] += tank.battles
            
            self.avg_tier = float(total_tier) / float(player.overall.battles)

    def report(self):
        if self.player.error != "":
            return "Could not find this player :fearful:"

        verdict = self.verdict()

        return (f":thinking: My verdict for {self.player.name}:\n"
                  f"```{verdict}```")
    
    def verdict(self):
        if self.player.overall.battles == 0:
            return "This player has 0 battles, so I guess he's just an asshole ¯\_(ツ)_/¯"

        if self.avg_tier < 5.0:
            return "Filthy low tier sealclubber"
        else:
            most_played_type = max(self.tank_types, key=self.tank_types.get)
            if most_played_type == TankClass.TD:
                return "Redline bush wanker"
            elif most_played_type == TankClass.SPG:
                return "Point & Click adventure gamer"
            elif most_played_type == TankClass.HT:
                return "Braindead heavy driver"
            elif most_played_type == TankClass.MT:
                return "Noob mediums, why u run away from fight"
            elif most_played_type == TankClass.LT:
                return "Filthy light tank WN8 stetpedder"
def classify_player(html):
    soup = BeautifulSoup(html, "html.parser")
    player = Player(soup)
    stats = PlayerClassification(player)
    return stats.report()

def main():
    file = open("sample.html")
    print(classify_player(file.read()))

if __name__ == "__main__":
    main()

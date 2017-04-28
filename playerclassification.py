from player import Player, PeriodStats
from tank import Tank, TankClass

def all_classifiers():
    return [AppTuxClassification,
            Clicker,
            SealClubber,
            RerollClassification,
            NewNoob,
            IsBot,
            BrainDead,
            BraindeadHeavy,
            RedlinePadder,
            BushWanker,
            AverageBob,
            GreenLeaf,
            NotEvenBlue,
            BlueFaggot,
            PurplePadder]

class Classifier:
    player: Player

    def __init__(self, player: Player):
        self.player = player
    
    def rate(self):
        raise NotImplementedError

    def verdict(self):
        raise NotImplementedError

class AppTuxClassification(Classifier):
    def rate(self):
        return self.player.name == "AppTux"

    def verdict(self):
        return "Super amazing, best player in the world!"

class NotEvenBlue(Classifier):
    def rate(self):
        return 1800.0 < self.player.overall.wn8 < 2200.0

    def verdict(self):
        return "Oh my god you're so bad you can't even be blue"

class BlueFaggot(Classifier):
    def rate(self):
        return 2200.0 < self.player.overall.wn8 < 2500.0

    def verdict(self):
        return "Blue faggot, wants to be purple but will never achieve it"

class RerollClassification(Classifier):
    def rate(self):
        # you rate high (+1) if you have <5k battles and >2.5k wn8,
        return self.player.overall.battles < 5000 and self.player.overall.wn8 > 2500.0 and self.player.overall.avg_tier > 6.0
    
    def verdict(self):
        return "Fucking filthy reroll slut, you like e-peen that much?"

class NewNoob(Classifier):
    def rate(self):
        return self.player.overall.battles < 3000

    def verdict(self):
        return "Fresh meat, feast away"

class Clicker(Classifier):
    def rate(self):
        spg_battles = self.player.classes[TankClass.SPG]

        return (spg_battles / self.player.overall.battles) > 0.2

    def verdict(self):
        return "Point & Click adventure gamer"

class BrainDead(Classifier):
    def rate(self):
        return self.player.overall.battles > 10000 and self.player.overall.wn8 < 800.0

    def verdict(self):
        return f"Confirmed braindead, only {self.player.overall.wn8} WN8 after {self.player.overall.battles} battles."

class RedlinePadder(Classifier):
    def rate(self):
        wn8 = self.player.overall.wn8
        wr = self.player.overall.winrate

        return (2000.0 <= wn8 <= 3000.0) and wr < 54.0
    
    def verdict(self):
        return "Redline WN8 padder"

class IsBot(Classifier):
    def rate(self):
        return self.player.overall.battles > 15000 and self.player.overall.winrate < 45.0

    def verdict(self):
        return "Hmm, a bot is better"

class PurplePadder(Classifier):
    def rate(self):
        return self.player.overall.battles > 15000 and self.player.overall.wn8 > 3000.0

    def verdict(self):
        return "OMG PURPLE NOOB PLAYER HE ONLY CARES ABOUT WN8"

class BushWanker(Classifier):
    def rate(self):
        td_battles = self.player.classes[TankClass.TD]

        return (td_battles / self.player.overall.battles) > 0.25

    def verdict(self):
        return "Redline bush wanker"

class BraindeadHeavy(Classifier):
    def rate(self):
        ht_battles = self.player.classes[TankClass.HT]

        return (ht_battles / self.player.overall.battles) > 0.25 and self.player.overall.winrate < 49.0

    def verdict(self):
        return "Braindead heavy driver"

class SealClubber(Classifier):
    def rate(self):
        return self.player.overall.avg_tier < 5.0 and self.player.overall.battles > 5000

    def verdict(self):
        return "Filthy low-tier sealclubber"

class AverageBob(Classifier):
    def rate(self):
        return 800.0 <= self.player.overall.wn8 <= 1200.0

    def verdict(self):
        return "Just your average bob, fucking casuals man"

class GreenLeaf(Classifier):
    def rate(self):
        return 1200.0 <= self.player.overall.wn8 <= 1800.0

    def verdict(self):
        return "Give your PC to a refugee, he can do better"

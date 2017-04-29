from player import Player, PeriodStats
from tank import Tank, TankClass

def all_classifiers():
    return [AppTux,
            Noxus,
            Clicker,
            Siemka,
            LowePlayer,
            VeryLowTierPadder,
            SealClubber,
            Reroll,
            NewNoob,
            BrainDead,
            BraindeadHeavy,
            RedlinePadder,
            LightPadder,
            BushWanker,
            IsBot,
            QBIsGod,
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

class AppTux(Classifier):
    def rate(self):
        return self.player.name == "AppTux"

    def verdict(self):
        return "Super amazing, best player in the world!"

class Noxus(Classifier):
    def rate(self):
        return self.player.name == "Noxusrevenge"

    def verdict(self):
        return "Loves penis"

class Siemka(Classifier):
    def rate(self):
        return "pl" in self.player.name

    def verdict(self):
        return "Looks siemka pl to me"

class VeryLowTierPadder(Classifier):
    lowtier_battles: int

    def rate(self):
        # we let players with <4k battles slide
        if self.player.overall.battles < 4000:
            return False

        self.lowtier_battles = sum([self.player.tiers[x] for x in range(1, 4)])

        percentage_lowtiers = self.lowtier_battles / self.player.overall.battles

        return percentage_lowtiers > 0.25

    def verdict(self):
        return f"How the fuck do manage to play {self.lowtier_battles} battles in tier 1-3"

class LowePlayer(Classifier):
    def rate(self):
        # have no tanks t5-7 but do have t8s
        mid_tiers = sum([self.player.tiers[x] for x in range(5, 8)])
        t8 = self.player.tiers[8]

        return mid_tiers == 0 and t8 > 0

    def verdict(self):
        return "Yeah.... Buying t8 premiums without having a normal t8 doesn't make you better at the game"

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

class Reroll(Classifier):
    def rate(self):
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

        return (wn8 > 2000.0) and wr < 54.0
    
    def verdict(self):
        return "Redline WN8 padder"

class IsBot(Classifier):
    def rate(self):
        return self.player.overall.battles > 15000 and self.player.overall.winrate < 45.0

    def verdict(self):
        return "Hmm, a bot is better"

class PurplePadder(Classifier):
    def rate(self):
        return self.player.overall.battles > 15000 and self.player.overall.wn8 > 2500.0

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

class QBIsGod(Classifier):
    def rate(self):
        return 1000.0 <= self.player.overall.wn8 <= 1100.0

    def verdict(self):
        return "Thanks to QB I finally have over 1k wn8, I'm god tier player now"

class AverageBob(Classifier):
    def rate(self):
        return 800.0 <= self.player.overall.wn8 <= 1200.0

    def verdict(self):
        return "So fucking average I can't even think of a special insult for you"

class GreenLeaf(Classifier):
    def rate(self):
        return 1200.0 <= self.player.overall.wn8 <= 1800.0

    def verdict(self):
        return "Give your PC to a refugee, he can do better"

class LightPadder(Classifier):
    def rate(self):
        lt_battles = self.player.classes[TankClass.LT]

        return (lt_battles / self.player.overall.battles) > 0.25 and self.player.overall.wn8 > 2200.0

    def verdict(self):
        return "Light tank WN8 pedder"

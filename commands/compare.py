from bs4 import BeautifulSoup
from wotlife.player import Player
from wotlife.tank import Tank, TankClass

class PlayerComparission:
	player1: Player
	player2: Player
	username1: str
	username2: str
	result: str
	
	def __init__(self, player1: Player, player2: Player, username1: str, username2: str):
		self.player1 = player1
		self.player2 = player2
		self.username1 = username1
		self.username2 = username2
		self.result = " "
		
		if player1.error != " ":
			return
		elif player2.error != " ":
			return
	def report(self):
		if self.player1.error != " ":
			return f"Could not find {self.username1} :fearful:"
		elif self.player2.error != " ":
			return f"Could not find {self.username2} :fearful:"
		return (f":thinking: My verdict for {self.player1.name} and {self.player2.name} :\n"
                  f"```{verdict}```")
			
	def verdict(self):
		if self.player1.overall.wn8 > self.player2.overall.wn8:
			result += "{self.player1.name clubs more seals ({self.player1.overall.wn8} to {self.player2.overall.wn8} WN8) \n"
		else:
			result += "{self.player2.name clubs more seals ({self.player1.overall.wn8} to {self.player2.overall.wn8} WN8) \n"
		
		if self.player1.overall.winrate < self.player1.overall.winrate:
			result += "{self.player1.name snipes from the red line ({self.player1.overall.winrate}% to {self.player2.overall.winrate}%) \n"
		else:
			result += "{self.player2.name snipes from the red line ({self.player1.overall.winrate}% to {self.player2.overall.winrate}%) \n"
			
		if self.player1.overall.battles > self.player2.overall.battles:
			result += "{self.player1.name has no life ({self.player1.overall.battles}% to {self.player2.overall.battles} battles)% \n"
		else:
			result += "{self.player2.name has no life ({self.player1.overall.battles}% to {self.player2.overall.battles} battles)% \n"
		
		if (self.player1.classes[TankClass.HT]/self.player1.overall.battles) > (self.player2.classes[TankClass.HT]/self.player2.overall.battles):
			result += "{self.player1.name is more braindead} \n"
		else:
			result += "{self.player2.name is more braindead} \n"
			
		if (self.player1.classes[TankClass.LT]/self.player1.overall.battles) > (self.player2.classes[TankClass.LT]/self.player2.overall.battles):
			result += "{self.player1.name pads his stats in lights} \n"
		else:
			result += "{self.player2.name pads his stats in lights} \n"
		
		if (self.player1.classes[TankClass.MT]/self.player1.overall.battles) > (self.player2.classes[TankClass.MT]/self.player2.overall.battles):
			result += "{self.player1.name runs away more often} \n"
		else:
			result += "{self.player2.name runs away more often} \n"
		
		if (self.player1.classes[TankClass.TD]/self.player1.overall.battles) > (self.player2.classes[TankClass.TD]/self.player2.overall.battles):
			result += "{self.player1.name wanks in a bush} \n"
		else:
			result += "{self.player2.name wanks in a bush} \n"
			
		if (self.player1.classes[TankClass.SPG]/self.player1.overall.battles) > (self.player2.classes[TankClass.SPG]/self.player2.overall.battles):
			result += "{self.player1.name is a filthy clicker} \n"
		else:
			result += "{self.player2.name is a filthy clicker} \n"
			
		return result		
		
def compare_players(html, "html.parser"):
	soup = BeautifulSoup(html, "html.parser")
    player = Player(soup)
    stats = PlayerComparission(player, username)
    return stats.report()

#dunno if needed, delete if you want to	
def main():
    file = open("sample.html")
    print(classify_player(file.read()))

if __name__ == "__main__":
    main()
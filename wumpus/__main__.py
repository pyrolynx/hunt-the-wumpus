from wumpus.game import Game
from wumpus.controller import CLIController

game = Game(controller=CLIController())
game.prepare()
game.run()

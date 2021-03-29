from wumpus.controller import CLIController
from wumpus.game import Game
from wumpus.map import DecaMap

try:
    game_map = DecaMap()
    game = Game(controller=CLIController(), map=game_map)
    game.prepare()
    game.run()
except (KeyboardInterrupt, EOFError):
    pass

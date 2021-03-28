class Room:
    _game: "Game"
    sign: str = None
    lose_reason: str = None

    def __init__(self, game: "Game"):
        self._game = game

    def on_enter(self):
        return

    def on_shot(self):
        return


class BatsRoom(Room):
    sign: str = "YOU HEAR FLAPPING"

    def on_enter(self):
        self._game.teleport()


class PitRoom(Room):
    sign: str = "YOU FEEL A BREEZE"
    lose_reason: str = "YOU FALL IN PIT"

    def on_enter(self):
        return False


class WumpusRoom(Room):
    sign: str = "YOU SMELL A WUMPUS"
    lose_reason: str = "WUMPUS ATE YOU"

    def on_enter(self):
        return False

    def on_shot(self):
        return True

class GameError(Exception):
    pass


class WinGame(GameError):
    pass


class LoseGame(GameError):
    reason: str

    def __init__(self, reason: str):
        self.reason = reason


class ControllerError(GameError):
    pass


class InvalidInput(GameError):
    pass

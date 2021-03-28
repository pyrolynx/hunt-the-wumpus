from abc import ABC, abstractmethod
from typing import List

from wumpus.const import ActionType


class Controller(ABC):
    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def lose(self, reason: str):
        raise NotImplementedError

    @abstractmethod
    def win(self):
        raise NotImplementedError

    @abstractmethod
    def choose_action(self) -> ActionType:
        raise NotImplementedError

    @abstractmethod
    def choose_direction(self, options: List[int]) -> int:
        raise NotImplementedError

    @abstractmethod
    def display_room(self, room_id: int, *signs: str):
        raise NotImplementedError

    @abstractmethod
    def teleport(self):
        raise NotImplementedError

    @abstractmethod
    def shot_missed(self, remaining_arrows: int):
        raise NotImplementedError


class CLIController(Controller):
    @staticmethod
    def display_text(text: str):
        print(text)
        print()

    @staticmethod
    def enter_value():
        return input("> ")

    def error(self, message: str):
        self.display_text(f"ERROR: {message}")

    def start(self):
        self.display_text("HUNT THE WUMPUS")

    def win(self):
        self.display_text("YOU WIN!\nWAMPUS DEFEATED")

    def lose(self, reason: str):
        self.display_text(f"YOU LOSE!\n{reason.upper()}")

    def choose_action(self) -> ActionType:
        action_options = [f"{action.name} ({action.value})" for action in ActionType]

        self.display_text(f"CHOOSE ACTION: {', '.join(action_options)}?")
        try:
            return ActionType(self.enter_value())
        except ValueError:
            raise

    def choose_direction(self, options: List[int]) -> int:
        self.display_text(f"CHOOSE ROOM: {', '.join([str(x) for x in options])}?")
        try:
            room = int(self.enter_value())
            assert room in options
            return room
        except ValueError:
            raise

    def display_room(self, room_id: int, *signs: str):
        self.display_text("\n".join([f"YOU ARE IN ROOM {room_id}", *signs]))

    def teleport(self):
        self.display_text("BATS GRAB YOU AND MOVE TO ANOTHER ROOM")

    def shot_missed(self, remaining_arrows: int):
        self.display_text(f"ARROW MISSED! NOW YOU HAVE {remaining_arrows} ARROWS")

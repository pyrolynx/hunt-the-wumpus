import random

from wumpus import DecaMap, DecaNode, WumpusRoom, PitRoom, BatsRoom
from wumpus.controller import Controller
from wumpus.const import ActionType
from wumpus.room import Room

PIT_ROOMS = 3
BATS_ROOMS = 3
ARROWS = 5


class GameError(Exception):
    pass


class WinGame(GameError):
    pass


class LoseGame(GameError):
    reason: str

    def __init__(self, reason: str):
        self.reason = reason


class Game:
    map: DecaMap
    wumpus_node: DecaNode
    player_node: DecaNode
    arrows: int = ARROWS
    controller: Controller

    def __init__(self, controller: Controller):
        self.controller = controller

    def prepare(self):
        self.map = DecaMap()
        self.map.fill()
        self.wumpus_node, self.player_node, *traps_nodes = random.choices(
            self.map.nodes, k=PIT_ROOMS + BATS_ROOMS + 2
        )
        self.wumpus_node.room = WumpusRoom(self)
        for _ in range(PIT_ROOMS):
            traps_nodes.pop().room = PitRoom(self)
        for _ in range(BATS_ROOMS):
            traps_nodes.pop().room = BatsRoom(self)
        for node in self.map.nodes:
            if node.room is None:
                node.room = Room(self)

    def run(self):
        self.controller.start()
        try:
            while self.arrows > 0:
                self.controller.display_room(
                    self.player_node.id,
                    *[
                        # node.room.sign
                        f"[DEBUG] {node.room.sign} ({node.id}, {node.__class__.__name__})"
                        for node in self.player_node.neighborhoods
                        if node.room.sign is not None
                    ],
                )
                action = self.controller.choose_action()
                direction = self.controller.choose_direction(
                    [node.id for node in self.player_node.neighborhoods]
                )
                if action == ActionType.MOVE:
                    self.move_player(self.map[direction])
                elif action == ActionType.SHOT:
                    self.arrows -= 1
                    self.shot(self.map[direction])
                    self.controller.shot_missed(self.arrows)
                else:
                    raise RuntimeError
            else:
                raise LoseGame("YOU SPEND ALL ARROWS")
        except WinGame:
            self.controller.win()
        except LoseGame as e:
            self.controller.lose(e.reason)

    def shot(self, node: DecaNode):
        if isinstance(node.room, WumpusRoom):
            raise WinGame

    def move_player(self, node: DecaNode):
        self.player_node = node
        state = self.player_node.room.on_enter()
        if state is None:
            return
        elif state:
            raise WinGame
        else:
            raise LoseGame(self.player_node.room.lose_reason)

    def teleport(self):
        node = random.choice([node for node in self.map.nodes if node != self.player_node])
        print(f"[DEBUG] Teleporting to ({node.id}, {node.__class__.__name__})")
        self.move_player(
            node
        )

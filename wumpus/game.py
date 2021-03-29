import random

from wumpus.const import ActionType
from wumpus.controller import Controller
from wumpus.errors import LoseGame, WinGame
from wumpus.map import Map, Node
from wumpus.room import BatsRoom, PitRoom, Room, WumpusRoom

PIT_ROOMS = 3
BATS_ROOMS = 3
ARROWS = 2


class Game:
    map: Map
    wumpus_node: Node
    player_node: Node
    arrows: int = ARROWS
    controller: Controller

    def __init__(self, controller: Controller, map: Map):
        self.controller = controller
        self.map = map

    def prepare(self):
        self.map.fill()
        self.wumpus_node, self.player_node, *traps_nodes = random.sample(
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
                        node.room.sign
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

    def shot(self, node: Node):
        if isinstance(node.room, WumpusRoom):
            raise WinGame

    def move_player(self, node: Node):
        self.player_node = node
        state = self.player_node.room.on_enter()
        if state is None:
            return
        elif state:
            raise WinGame
        else:
            raise LoseGame(self.player_node.room.lose_reason)

    def teleport(self):
        self.controller.teleport()
        self.move_player(
            random.choice(
                [node for node in self.map.nodes if node != self.player_node]
            )
        )

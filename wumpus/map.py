from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

from wumpus.room import Room


@dataclass
class Node:
    id: int
    room: "Room" = None

    _neighborhoods = None

    def __post_init__(self):
        self._neighborhoods = set()

    @property
    def neighborhoods(self):
        return set(self._neighborhoods)

    def connect(self, node: "Node"):
        assert len(self._neighborhoods) < 3 and len(node._neighborhoods) < 3, (
            self._neighborhoods,
            node._neighborhoods,
        )
        assert (
            node not in self._neighborhoods and self not in node._neighborhoods
        )
        self._neighborhoods.add(node)
        node._neighborhoods.add(self)

    def __hash__(self):
        return self.id

    def __eq__(self, other: "Node"):
        return self.id == other.id


class Map(ABC):
    @property
    @abstractmethod
    def nodes(self) -> List[Node]:
        raise NotImplementedError

    @abstractmethod
    def fill(self):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, node_id: int):
        raise NotImplementedError


class DecaMap(Map):
    _nodes: Dict[int, Node]

    def __init__(self):
        self._nodes = {}

    @property
    def nodes(self) -> List[Node]:
        return list(self._nodes.values())

    def __getitem__(self, node_id):
        return self._nodes[node_id]

    def fill(self):
        nodes = [Node(i) for i in range(1, 21)]

        top_layer, middle_layer, bottom_layer = (
            nodes[:5],
            nodes[5:15],
            nodes[15:],
        )
        for i in range(5):
            top_layer[i].connect(top_layer[(i + 1) % 5])
            bottom_layer[i].connect(bottom_layer[(i + 1) % 5])

        for i in range(10):
            middle_layer[i].connect(middle_layer[(i + 1) % 10])

        layer, next_layer = top_layer, bottom_layer
        for node in middle_layer:
            node.connect(layer.pop(0))
            layer, next_layer = next_layer, layer

        assert all(len(node.neighborhoods) == 3 for node in nodes)
        for node in nodes:
            self._nodes[node.id] = node

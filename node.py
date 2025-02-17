from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Node():
    """
    """

    binary_id: Optional[bool] = field(default=None, init=False)
    chars:List[str] = field(default_factory=list, init=False)

    probability: float = field(default=0.0)

@dataclass
class Leaf(Node):
    """
    """

    char:Optional[str] = None

    def __post_init__(self):
        self.chars = [self.char]


@dataclass
class Inner(Node):
    """
    """

    first_child_node: Optional[Node] = None
    second_child_node: Optional[Node] = None

    def __post_init__(self):

        if self.first_child_node and self.second_child_node:
            self.probability = self.first_child_node.probability + self.second_child_node.probability
            self.chars = self.first_child_node.chars + self.second_child_node.chars
            self.first_child_node.binary_id = 0
            self.second_child_node.binary_id = 1


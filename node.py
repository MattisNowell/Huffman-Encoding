class Node:
    """
    """
    binary_id: bool = 0
    probability: float = 0.0
    
    first_child_node: "Node" = None
    second_child_node: "Node" = None

    def __init__(self, first_child_node: "Node" = None, second_child_node: "Node" = None, character: chr = None,
                 probability: float = 0.0):
        if character is not None and probability != 0.0:
            self.first_child_node = None
            self.second_child_node = None
            self.probability = probability
            self.chars: list = []
            self.chars.append(character)
        else:
            self.first_child_node = first_child_node
            self.second_child_node = second_child_node
            self.probability = first_child_node.probability + second_child_node.probability
            self.chars = first_child_node.chars + second_child_node.chars
            first_child_node.binary_id = 0
            second_child_node.binary_id = 1
            
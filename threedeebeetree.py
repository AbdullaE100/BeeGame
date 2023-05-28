from __future__ import annotations
from typing import Dict, Generic, Optional, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:
    key: Point
    item: I
    subtree_size: int = 1
    children: Dict[int, BeeNode] = field(default_factory=dict)

    def get_child_for_key(self, point: Point) -> Optional[BeeNode]:
        """
        Returns the child node associated with the given point.

Input: point (Tuple of int) - The point for which the associated child node is to be found.
Output: BeeNode object or None - The child node associated with the given point, if it exists. If it does not exist, None is returned.
Complexity: O(1) - Constant time complexity since it is directly accessing a dictionary.
        """
        idx = self.get_octant_idx_for_point(point)
        return self.children.get(idx)

    def get_octant_idx_for_point(self, point: Point) -> int:
        """
        Returns the octant index for a given point.

Input: point (Tuple of int) - The point for which the octant index is to be found.
Output: int - The octant index for the given point.
Complexity: O(1) - Constant time complexity since we are simply comparing the coordinates and returning an integer value.
        
        """
        idx = 0
        if point[0] >= self.key[0]: idx |= 4
        if point[1] >= self.key[1]: idx |= 2
        if point[2] >= self.key[2]: idx |= 1
        return idx


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
            Checks whether the tree is empty or not.

Output: bool - True if the tree is empty, False otherwise.
Complexity: O(1) - Constant time complexity because we're only checking the length of the tree.
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree.
        Returns the number of nodes in the tree.

Output: int - The number of nodes in the tree.
Complexity: O(1) - Constant time complexity because we're only returning the length of the tree.
         """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
            Checks whether a given key exists in the tree or not.

Input: key (Tuple of int) - The key to be checked.
Output: bool - True if the key exists in the tree, False otherwise.
Complexity: O(log(n)) - Logarithmic time complexity because in the worst case we might need to traverse the entire height of the tree.
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            Returns the item associated with the given key.

Input: key (Tuple of int) - The key for which the item is to be found.
Output: The item associated with the key.
Complexity: O(log(n)) - Logarithmic time complexity because in the worst case we might need to traverse the entire height of the tree.
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        Returns the node associated with the given key.

Input: key (Tuple of int) - The key for which the node is to be found.
Output: BeeNode - The node associated with the key.
Complexity: O(log(n)) - Logarithmic time complexity because in the worst case we might need to traverse the entire height of the tree.

        
        """
        if self.root is None:
            raise KeyError(f"Key not found: {key}")

        node = self.root
        while True:
            idx = node.get_octant_idx_for_point(key)
            if node.key == key:
                return node
            elif idx in node.children:
                node = node.children[idx]
            else:
                raise KeyError(f"Key not found: {key}")

    def __setitem__(self, key: Point, item: I) -> None:
        """
        
        Inserts the item into the tree at the given key.

Input: key (Tuple of int) - The key at which the item is to be inserted.
Input: item - The item to be inserted.
Complexity: O(log(n)) - Logarithmic time complexity because in the worst case we might need to traverse the entire height of the tree.
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            Attempts to insert an item into the tree.

Input: current (BeeNode) - The current node.
Input: key (Tuple of int) - The key at which the item is to be inserted.
Input: item - The item to be inserted.
Output: BeeNode - The node after the item has been inserted.
Complexity: O(log(n)) - Logarithmic time complexity because in the worst case we might need to traverse the entire height of the tree.

        """
        if current is None:
            self.length += 1
            return BeeNode(key, item)

        idx = current.get_octant_idx_for_point(key)
        if current.key == key:
            current.item = item  # replace item for existing key
        elif idx in current.children:
            current.children[idx] = self.insert_aux(current.children[idx], key, item)
        else:
            current.children[idx] = BeeNode(key, item)

        current.subtree_size = 1 + sum(c.subtree_size for c in current.children.values())
        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. 
        Checks whether the given node is a leaf or not.

Input: current (BeeNode) - The node to be checked.
Output: bool - True if the node is a leaf, False otherwise.
Complexity: O(1) - Constant time complexity because we're only checking the children of the node.
"""
        return not bool(current.children)

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2

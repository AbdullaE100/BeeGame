""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations
from typing import Optional


__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Overriding the method to maintain subtree_size field
        """
        if current is None:
            self.length += 1
            return TreeNode(key, item=item, subtree_size=1)

        if key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:
            raise ValueError('Inserting duplicate item')

        current.subtree_size = 1 + (current.left.subtree_size if current.left else 0) + \
                            (current.right.subtree_size if current.right else 0)

        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Overriding the method to maintain subtree_size field
        """
        if current is None:
            raise ValueError('Deleting non-existent item')

        if key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        current.subtree_size = 1 + (current.left.subtree_size if current.left else 0) + \
                            (current.right.subtree_size if current.right else 0)

        return current


    def get_successor(self, node: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Get successor of the current node.

        The successor of a node in a Binary Search Tree (BST) is defined as 
        the node with the smallest key greater than the current node's key 
        within the current node's right subtree. If the current node doesn't 
        have a right child, it returns None, indicating no successor exists 
        within its own subtree.

        Parameters:
        node (TreeNode): The node for which the successor is to be found.

        Returns:
        TreeNode: The successor of the current node. If no successor exists, returns None.

        :complexity: The time complexity is O(h), where h is the height of the tree. 
        In the worst case, this function will have to travel down the height 
        of the tree to find the successor. 
        """
        if node is None:
            return None

        if node.right is not None:
            return self.get_minimal(node.right)

        return None


    def get_minimal(self, current: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Get the node with the smallest key in the current sub-tree.

        It traverses to the leftmost node in the sub-tree of the current node, 
        as in a BST, the node with the smallest key is always located at the leftmost. 
        If the current node is None, it returns None.

        Parameters:
        current (TreeNode): The root of the subtree in which the minimum key node is to be found.

        Returns:
        TreeNode: The node with the smallest key in the sub-tree. If the sub-tree is empty, returns None.

        :complexity: The time complexity is O(h), where h is the height of the tree. 
        In the worst case, this function will have to travel down the height 
        of the tree to find the node with the smallest key.
        """
        if current is None:
            return None

        while current.left is not None:
            current = current.left

        return current


    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Finds the kth smallest node by key in the subtree rooted at the current node.

        The function takes in an integer k and a TreeNode current. It then recursively 
        searches for the kth smallest node in the subtree with 'current' as the root. 
        If current is None or if k is larger than the size of the tree rooted at current, 
        it returns None.

        Parameters:
        k (int): The rank of the node to be found in the ordered sequence of nodes.
        current (Optional[TreeNode]): The root of the subtree in which to search for the kth smallest node.

        Returns:
        Optional[TreeNode]: The kth smallest node by key in the subtree. If no such node exists, returns None.

        :complexity: The time complexity is O(h), where h is the height of the tree. 
        In the worst case, this function will have to travel down the height 
        of the tree to find the kth smallest node. This assumes that the subtree_size 
        field is being properly maintained.
        """
        if current is None:
            return None

        left_size = current.left.subtree_size if current.left else 0

        if k == left_size + 1:  # current is the kth node
            return current
        elif k <= left_size:  # the kth node is in the left subtree
            return self.kth_smallest(k, current.left)
        else:  # the kth node is in the right subtree
            return self.kth_smallest(k - left_size - 1, current.right)

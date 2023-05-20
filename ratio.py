from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree


T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        Initialises an empty binary search tree as the percentile object

        Best Case - O(1), since initialisation of empty binary search tree is constant

        Worst Case - same as best case
        """

        # Using a binary search tree as the store for the points
        self.store : BinarySearchTree = BinarySearchTree()
    
    def add_point(self, item: T) -> None:
        """
        Adding a point from the object

        Best Case -  O(CompK) inserts the item at the root.
            
        Worst case - O(CompK * D) inserting at the bottom of the tree
            
        where D is the depth of the tree
        CompK is the complexity of comparing the keys

        """
        # The key, value pair is the same
        self.store[item] = item
    
    def remove_point(self, item: T) -> None:
        """
        Removing a point from the object

        Best Case -  O(CompK) deleting the item at the root.
            
        Worst case - ***complete***
            
        where D is the depth of the tree
        CompK is the complexity of comparing the keys

        """
        # delete the node from the binary tree
        del self.store[item]
    

    def ratio(self, x, y) -> list[int]:
        """
        Returns a list that satisfies the ratio requirements

        Best Case -  ***complete***
            
        Worst case - ***complete***
            
        where D is the depth of the tree
        CompK is the complexity of comparing the keys

        """
        # calculating the treshholds for x and y
        threshold_x_element : int = ceil(x*(len(self.store)))    #O(1)
        threshold_y_element : int = ceil(y*(len(self.store)))    

        #calcuting the kth smallest elements for the thresholds
        """
        remember that kth_smallest returns the node and not the item itself
        """
        threshold_x = self.store.kth_smallest(threshold_x_element, self.store.root) #O(D), D is depth
        threshold_y = self.store.kth_smallest(threshold_y_element, self.store.root)

        
        lst = []
        final_list = self.aux_ratio(self.store.root, threshold_x.item, threshold_y.item, lst)
        return final_list
    
    def aux_ratio(self, current_node, x, y, lst) -> list[int]:
        if current_node is not None:
            
            if (x <= current_node.key):
                self.aux_ratio(current_node.left, x, y, lst)
            if ((current_node.key >= x) and (current_node.key <= y)):
                lst.append(current_node.key)
            if (y > current_node.key):
                self.aux_ratio(current_node.right, x, y, lst)
            
            
            
        return lst










if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))

    

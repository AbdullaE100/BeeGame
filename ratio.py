from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")


class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        Initializes a new percentiles object.
        """
        self.items = BinarySearchTree()
        self.size = 0

    def add_point(self, item: T):
        """
        Adds an item to the percentiles.

        Args:
            item: The item to add.
        """
        self.items[item] = item
        self.size += 1

    def remove_point(self, item: T):
        """
        Removes an item from the percentiles.

        Args:
            item: The item to remove.
        """
        del self.items[item]

    def ratio(self, x, y) -> list[T]:
        """
        Returns a list of items that are between the xth and yth percentiles.

        Args:
            x: The xth percentile.
            y: The yth percentile.

        Returns:
            A list of items that are between the xth and yth percentiles.
            
        Time complexities:
        Best case: O(log n), where n is the number of items in the percentiles.
        Worst case: O(n), where n is the number of items in the percentiles.

        """
        front = ceil((x / 100) * len(self.items))
        rear = ceil((y / 100) * len(self.items))
        elements = []

        while front < (len(self.items) - rear):
            item = self.items.kth_smallest(front + 1, self.items.root)
            elements.append(item.item)
            front += 1

        return elements


if __name__ == "__main__":
    points = list(range(50))
    import random

    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
    

from __future__ import annotations
from typing import List
from threedeebeetree import Point

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:

    def recursive_build(indices, depth=0):
        print(f"indices: {indices}, type: {type(indices)}")

        # Base case: if there's only one point or no point, return it
        if len(indices) == 0:
            return []
        elif len(indices) == 1:
            return [indices[0]]

        # Choose the splitting dimension based on the current depth
        dim = depth % 3

        # Sort the points based on the splitting dimension
        indices.sort(key=lambda i: my_coordinate_list[i][dim])

        # Find the median point and add it to the ordering
        median_idx = len(indices) // 2

        # adjust median if it falls into a group of same values to avoid skewness
        while median_idx < len(indices) - 1 and my_coordinate_list[indices[median_idx]][dim] == my_coordinate_list[indices[median_idx+1]][dim]:
            median_idx += 1
        # If the number of same values is greater than half of the list, then move the median back to create a better balance
        while median_idx > 0 and my_coordinate_list[indices[median_idx]][dim] == my_coordinate_list[indices[median_idx-1]][dim]:
            median_idx -= 1

        ordering = [indices[median_idx]]

        # Recursively build the left and right subtrees
        left_subtree = recursive_build(indices[:median_idx], depth + 1)
        right_subtree = recursive_build(indices[median_idx + 1:], depth + 1)

        # Return the ordering
        return ordering + left_subtree + right_subtree

    # Build the ordering recursively
    return [my_coordinate_list[i] for i in recursive_build(list(range(len(my_coordinate_list))))]

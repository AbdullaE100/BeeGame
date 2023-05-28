from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Sorts a list of points by their x-coordinates.

    Args:
        my_coordinate_list: A list of points.

    Returns:
        A list of points sorted by their x-coordinates.

    Time complexity:
        O(n) in the best case and O(n^2) in the worst case, where n is the number of points in the list.
    """

    # Check if the list is empty. If it is, return an empty list.
    if not my_coordinate_list:
        return []

    # Extract the x-coordinates from the coordinate list.
    coordinate_x = [point[0] for point in my_coordinate_list]

    # Create a Percentiles object and add the x-coordinates.
    percentiles = Percentiles()
    for coordinate in coordinate_x:
        percentiles.add_point(coordinate)

    # Determine the x-coordinate of the root node.
    if len(percentiles.store) == 0:
        return []

    root_x_values = percentiles.ratio(0, len(percentiles.store))
    if not root_x_values:
        return []

    x_root = root_x_values[0]

    # Sort the coordinate list based on the x-coordinate of the root node.
    ordered_coordinates = sorted(my_coordinate_list, key=lambda point: abs(point[0] - x_root))

    return ordered_coordinates
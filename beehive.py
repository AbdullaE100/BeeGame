from dataclasses import dataclass
from heap import MaxHeap

@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""


    def __gt__(self, other):
        return min(self.capacity, self.volume)*self.nutrient_factor > min(other.capacity, other.volume)*other.nutrient_factor
    
    def __ge__(self, other):
        return min(self.capacity, self.volume)*self.nutrient_factor >= min(other.capacity, other.volume)*other.nutrient_factor
    
    def __lt__(self, other):
        return min(self.capacity, self.volume)*self.nutrient_factor < min(other.capacity, other.volume)*other.nutrient_factor
    
    def __le__(self, other):
        return min(self.capacity, self.volume)*self.nutrient_factor <= min(other.capacity, other.volume)*other.nutrient_factor
    
    def __eq__(self, other):
        return min(self.capacity, self.volume)*self.nutrient_factor == min(other.capacity, other.volume)*other.nutrient_factor

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

class BeehiveSelector:

    def __init__(self, max_beehives: int):
        """
        Best Case -  ***complete***
            
        Worst case - ***complete***

        """
        # Use a heap to store 
        self.store = MaxHeap(max_beehives)
        self.max_elements = max_beehives

    def set_all_beehives(self, hive_list: 'list[Beehive]'):
        self.store = MaxHeap(self.max_elements)
        for beehive in hive_list:
            self.add_beehive(beehive)

    
    def add_beehive(self, hive: Beehive):
        self.store.add(hive)
    

    def harvest_best_beehive(self):
        max_beehive = self.store.get_max()
        emeralds = min(max_beehive.capacity, max_beehive.volume)*max_beehive.nutrient_factor
        if max_beehive.volume > max_beehive.capacity:
            max_beehive.volume -= max_beehive.capacity
        else:
            max_beehive.volume = 0
        self.add_beehive(max_beehive)
        return emeralds


        


        
        





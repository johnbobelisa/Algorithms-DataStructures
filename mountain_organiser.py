from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import mergesort
from algorithms.binary_search import binary_search
class MountainOrganiser:

    def __init__(self) -> None:
        self.organiser_list = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Finds the rank of the provided mountain given all mountains included so far.
        Raises KeyError if this mountain hasn't been added yet.
        
        Complexity:
        See binary_search 
        - Best case: O(1)
        - Worst case: O(log n)
        where n is the total number of mountains included so far 
        """ 
        mountain_rank = binary_search(self.organiser_list, mountain)    # O(log n)
        if mountain_rank == -1:     # O(1)
            raise KeyError(mountain)
        else:
            return mountain_rank
        
    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser
        
        Complexity:
        See binary_search 
        - O(m * log(m) + n): where m is the length of the input list and
        n is the total number of mountains included so far.
        - best case = worst case (no condition in the while loop ends it early)
        """
        new_mountains_sorted = mergesort(mountains)     # O(m * log(m))
        
        all_mountains_sorted = []   # new list to store all the mountains sorted
        
        index_a = 0     # index for self.organiser_list
        index_b = 0     # index for new_mountains_sorted
        
        # O(n): as n will keep getting bigger as more mountains are added,
        # where n is the total number of mountains included so far.
        while index_a < len(self.organiser_list) and index_b < len(new_mountains_sorted):
            if self.organiser_list[index_a] < new_mountains_sorted[index_b]:
                all_mountains_sorted.append(self.organiser_list[index_a])
                index_a += 1
            else: 
                all_mountains_sorted.append(new_mountains_sorted[index_b])
                index_b += 1
                
        if index_a < len(self.organiser_list):  # mountains remaining in self.organiser_list
            all_mountains_sorted += self.organiser_list[index_a:]
        elif index_b < len(new_mountains_sorted):   # mountains remaining in new_mountains_sorted
            all_mountains_sorted += new_mountains_sorted[index_b:]
            
        self.organiser_list = all_mountains_sorted
            

if __name__ == "__main__":
    m1 = Mountain("m1", 2, 2)
    m2 = Mountain("m2", 2, 9)
    m3 = Mountain("m3", 3, 6)
    m4 = Mountain("m4", 3, 1)
    m5 = Mountain("m5", 4, 6)
    m6 = Mountain("m6", 7, 3)
    m7 = Mountain("m7", 7, 7)
    m8 = Mountain("m8", 7, 8)
    m9 = Mountain("m9", 7, 6)
    m10 = Mountain("m10", 8, 4)
    
    mo = MountainOrganiser()
    mo.add_mountains([m1, m2])
    print(mo.organiser_list)

    mo.add_mountains([m4, m3])
    print(mo.organiser_list)

    mo.add_mountains([m5])
    print(mo.organiser_list)
    
    mo.add_mountains([m7, m9, m6, m8])
    print(mo.organiser_list)

    mo.cur_position(m10)
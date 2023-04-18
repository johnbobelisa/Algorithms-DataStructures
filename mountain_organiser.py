from __future__ import annotations

from mountain import Mountain
from algorithms import mergesort

class MountainOrganiser:
    
    def __init__(self) -> None:
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        mountain_lengths = []

        if mountain not in self.mountains:
            raise KeyError()
        
        for m in self.mountains:
            m:Mountain
            mountain_lengths.append((m.length, m.name))
            
        sorted_lst = mergesort.mergesort(mountain_lengths)
        
        for rank, values in enumerate(sorted_lst):
            if mountain.name == values[1]:
                return rank
             
    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains += mountains


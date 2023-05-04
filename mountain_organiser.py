from __future__ import annotations

from mountain import Mountain
from infinite_hash_table import InfiniteHashTable
from algorithms.mergesort import mergesort    
from algorithms.binary_search import *

class MountainOrganiser:

    def __init__(self) -> None:
        self.table = InfiniteHashTable()
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:

        if mountain not in self.table.current_table:
            raise KeyError()

        cur_idx = binary_search(self.table.current_table, mountain)
        return cur_idx
             
    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains += mountains
        for m in mountains:
            self.table[m.name] = m.length
        self.mountains = mergesort(self.mountains)
        self.table.current_table = self.mountains
        
    
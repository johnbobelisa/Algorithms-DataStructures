from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        mountain_lengths = []

        if mountain not in self.mountains:
            raise KeyError()
        
        for m in self.mountains:
            m:Mountain
            mountain_lengths.append((m.name,m.length))
            
        sorted_lst = merge_sort(mountain_lengths)
        
        for rank, values in enumerate(sorted_lst):
            if mountain.name == values[0]:
                return rank
             
    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains += mountains

def merge_sort(lst):
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    right = lst[mid:]
    left = lst[:mid]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left, right):
    outcome = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            outcome.append(left[i])
            i += 1
        else:
            outcome.append(right[j])
            j += 1

    outcome += left[i:]
    outcome += right[j:]

    return outcome
from __future__ import annotations
from dataclasses import dataclass
import functools
@functools.total_ordering
@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Mountain):
            if self.length == other.length:
                if self.name == other.name:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return NotImplemented
        
    def __lt__(self, other: object) -> bool:
        if isinstance(other, Mountain):
            if self.length < other.length:
                return True
            elif self.length == other.length:   # same length
                if self.name < other.name:    # compare by name
                    return True
                else:
                    return False
            else:
                return False
        else:
            return NotImplemented
        
        
if __name__ == "__main__":
    from algorithms.mergesort import mergesort
    m1 = Mountain("m1", 2, 2)
    m2 = Mountain("m2", 2, 9)
    m3 = Mountain("m3", 3, 2)
    print(m1 < m3)
    print(sorted([m1, m2, m3]))
    print(mergesort([m1, m2, m3]))

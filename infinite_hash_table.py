from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Initialise the Hash Table.
        """
        self.top_table = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = 0  # start at level 0
        self.current_table = self.top_table

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1
    
    def _infinite_probe(self, key: K, is_insert: bool) -> ArrayR:
        """
        Find the correct table for this key
        Changes self.level to the level the correct table is located.
        """
        current_table = self.top_table
        
        while True:
            position = self.hash(key)
            
            if current_table[position] is None:
                if is_insert:
                    return current_table
                else:
                    raise KeyError(key)
            
            # matching key
            elif current_table[position][0] == key:
                return current_table
            
            # conflict, (key, table) at position
            elif isinstance(current_table[position][1], ArrayR):
                self.level += 1  
                current_table = current_table[position][1]      # move to next hash table
                continue
            
            # conflict, another (key, value) at position
            else:
                if is_insert:
                    # Create new table and reinsert conflicting (key, value)
                    other_key, other_value = current_table[position]        # current_table[position] contains (key, value)
                    next_table = ArrayR(self.TABLE_SIZE)        # create another hash table
                    next_table_key = other_key[:self.level + 1] + '*'      # change key to k*, ke*, key*, based on the level  
                    current_table[position] = (next_table_key, next_table)     # change value to table  
                    self.level += 1
                    current_table = next_table      # move to next hash table
                    other_position = self.hash(other_key)
                    current_table[other_position] = (other_key, other_value)
                    continue
                else:
                    raise KeyError(key)
        
    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        current_table = self._infinite_probe(key, False)
        position = self.hash(key)
        self.level = 0      # reset self.level
        return current_table[position][1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        current_table = self._infinite_probe(key, True)
        position = self.hash(key)
        self.level = 0      # reset self.level
        
        if current_table[position] is None:   
            self.count += 1     
        
        current_table[position] = (key, value)
    

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __len__(self):
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        while True:
            for i in range(len(self.current_table)):
                print(f"Table[{i}] = {self.current_table[i]}") 
            try:   
                next_index = int(input("Choose the next table by its index: "))
                self.current_table = self.current_table[next_index][1]
            except (ValueError, IndexError):
                return "Ended"

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        locations = []
        self._infinite_probe(key, False)
        
        for i in range(self.level + 1):
            self.level = i
            locations.append(self.hash(key))
        
        self.level = 0      # reset self.level
        return locations
    
    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
        
if __name__ == "__main__":
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    ih["linked"] = 4
    ih["limp"] = 5
    ih["linger"] = 8
    print(ih)
    print(len(ih))
    print(ih.get_location("linger"))

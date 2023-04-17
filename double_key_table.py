from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        self.outer_table = LinearProbeTable(None)
        if sizes is not None:
            self.outer_table = LinearProbeTable(sizes)

        self.internal_sizes = internal_sizes

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        self.outer_table.hash = lambda k: self.hash1(k)
        position_outer = self.outer_table._linear_probe(key1, is_insert)
        inner_table = LinearProbeTable(self.internal_sizes)
        inner_table.hash = lambda k: self.hash2(k, inner_table)

        if self.outer_table.array[position_outer] is None: #If empty
            self.outer_table.array[position_outer] = (key1, inner_table)
            position_inner = inner_table._linear_probe(key2, is_insert)
            inner_table.array[position_inner] = (key2, None)
        else: #If key already exists in the outer table
            inner_table:LinearProbeTable = self.outer_table.array[position_outer][1]
            position_inner = inner_table._linear_probe(key2, is_insert)


        return (position_outer, position_inner)
    

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    yield self.outer_table.array[i][0]    # will raise StopIteration automatically
        else:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.outer_table.array[i][0] == key:
                        for k2 in self.outer_table.array[i][1].keys():    # use keys() from hash_table.py
                            yield k2    # will raise StopIteration automatically

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        list_of_keys = []

        if key is None:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    list_of_keys.append(self.outer_table.array[i][0])                    
        else:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.outer_table.array[i][0] == key:
                        list_of_keys = self.outer_table.array[i][1].keys()    # use keys() from hash_table.py
                        break
        
        return list_of_keys

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    inner_table = self.outer_table.array[i][1]
                    for value in inner_table.values():     # use values() from hash_table.py
                        yield value     # will raise StopIteration automatically
        else:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.outer_table.array[i][0] == key:
                        inner_table = self.outer_table.array[i][1]
                        for value in inner_table.values():     # use values() from hash_table.py
                            yield value     # will raise StopIteration automatically

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        list_of_values = []

        if key is None:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    inner_table = self.outer_table.array[i][1]
                    list_of_values.extend(inner_table.values())     # use values() from hash_table.py
        else:
            for i in range(self.table_size):  
                if self.outer_table.array[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.outer_table.array[i][0] == key:
                        inner_table = self.outer_table.array[i][1]
                        list_of_values.extend(inner_table.values())     # use values() from hash_table.py
                        break   
                      
        return list_of_values

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        index1, index2 = self._linear_probe(key[0], key[1], False)

        if self.outer_table.array[index1][0] == key[0]:
            inner_table:LinearProbeTable = self.outer_table.array[index1][1]
            if inner_table.array[index2][0] == key[1]:
                return inner_table.array[index2][1] 
        
        raise KeyError()

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        top_lvl_keys = self.keys(None)
        bot_lvl_keys = self.keys(key[0])

        if key[0] not in top_lvl_keys:
            self.outer_table.count += 1            

        self.outer_table.hash = lambda k: self.hash1(k)
        pos1, pos2 = self._linear_probe(key[0], key[1], True)
             
        inner_table:LinearProbeTable = self.outer_table.array[pos1][1]
        if key[1] not in bot_lvl_keys:
            inner_table.count += 1

        inner_table.array[pos2] = (key[1], data)

        if len(self) > self.table_size / 2:
            self._rehash()
        
        if inner_table.count > inner_table.table_size / 2:
            inner_table._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], True)

        inner_table:LinearProbeTable = self.outer_table.array[pos1][1]
        inner_table.array[pos2] = None
        inner_table.count -= 1

        if inner_table.count == 0:
            self.outer_table.array[pos1] = None
            self.outer_table.count -= 1
            

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.outer_table.array
        self.outer_table.size_index += 1
        if self.outer_table.size_index == len(self.outer_table.TABLE_SIZES):
            return
        self.outer_table.array = ArrayR(self.outer_table.TABLE_SIZES[self.outer_table.size_index])
        self.outer_table.count = 0

        for item in old_array:
            if item is not None:
                key1, inner_table = item
                for item1 in inner_table.array:
                    if item1 is not None:
                        key2, data = item1
                        self[key1, key2] = data
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.outer_table.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.outer_table.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
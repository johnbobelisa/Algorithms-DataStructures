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
        """
        Complexity:
        - O(n): As we are creating an array of size n, where n is a value in TABLE_SIZES
        - best case = worst case
        """
        
        if sizes is not None:
            self.TABLE_SIZES = sizes
        
        self.internal_table = LinearProbeTable(internal_sizes)
        
        self.size_index_outer = 0    # index for TABLE_SIZES
        self.array_outer = ArrayR(self.TABLE_SIZES[self.size_index_outer]) # outer hash table
        self.count_outer = 0     # number of (k1, sub_table) in array_outer
       

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

        Complexity:
        - Best Case: O(hash1(key1) + hash2(key2)), when the first and second position is empty.
        - Worst Case: O((hash1(key1) + N * comp(K1)) + (hash2(key2) + M * comp(K2)))
        """
        index1 = self.hash1(key1)
        sub_table:LinearProbeTable = None
        
        for i in range(self.table_size):    # self.table_size is the table size of the outer hash table
            # self.array_outer[index1] contains (k1, sub_table)
            if self.array_outer[index1] is None:     # if empty
                if is_insert:
                    sub_table = LinearProbeTable(self.internal_table.TABLE_SIZES)
                    self.array_outer[index1] = (key1, sub_table)
                    self.count_outer += 1
                    break
                else:
                    raise KeyError(key1)
            # self.array_outer[index1] contains (k1, sub_table)  
            elif self.array_outer[index1][0] == key1:   # elif key1 is found at index1
                sub_table = self.array_outer[index1][1]
                break
            else:
                if i == self.table_size - 1:    # looped to the end
                    if is_insert:
                        raise FullError("Table is full!")
                    else:
                        raise KeyError(key1)
                index1 = (index1 + 1) % self.table_size

        sub_table.hash = lambda k: self.hash2(k, sub_table)
        index2 = sub_table._linear_probe(key2, is_insert)
        
        return index1, index2

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        Complexity:
        - Best Case: O(n), occurs when key is None, where n is the table_size of the outer table.
        - Worst Case: O((n*comp(K1))*m), occurs when key is not None, where n is the table_size of 
        the outer table and m is the table size of the inner table. 
        """
        if key is None:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    yield self.array_outer[i][0]    # will raise StopIteration automatically
        else:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.array_outer[i][0] == key:
                        for k2 in self.array_outer[i][1].keys():    # use keys() from hash_table.py
                            yield k2    # will raise StopIteration automatically

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        Complexity:
        - Best Case: O(n), occurs when key is None, where n is the table size of the outer table.
        - Worst Case: O((n*comp(K1))*m), occurs when key is not None, where n is the table_size of 
        the outer table and m is the table_size of the inner table. 
        """
        list_of_keys = []

        if key is None:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    list_of_keys.append(self.array_outer[i][0])                    
        else:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.array_outer[i][0] == key:
                        list_of_keys = self.array_outer[i][1].keys()    # use keys() from hash_table.py
                        break
        
        return list_of_keys

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        Complexity:
        - Best Case: O(n), occurs when key is None, where n is the table size of the outer table.
        - Worst Case: O((n*comp(K1))*m), occurs when key is not None, where n is the table_size of 
        the outer table and m is the table_size of the inner table.
        """
        if key is None:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    inner_table = self.array_outer[i][1]
                    for value in inner_table.values():     # use values() from hash_table.py
                        yield value     # will raise StopIteration automatically
        else:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.array_outer[i][0] == key:
                        inner_table = self.array_outer[i][1]
                        for value in inner_table.values():     # use values() from hash_table.py
                            yield value     # will raise StopIteration automatically

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        Complexity:
        - Best Case: O(n), occurs when key is None, where n is the table size of the outer table.
        - Worst Case: O((n*comp(K1))*m), occurs when key is not None, where n is the table_size of 
        the outer table and m is the table_size of the inner table.
        """
        list_of_values = []

        if key is None:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    inner_table = self.array_outer[i][1]
                    list_of_values.extend(inner_table.values())     # use values() from hash_table.py
        else:
            for i in range(self.table_size):  
                if self.array_outer[i] is not None:     # self.array_outer[i] is (k1, sub_table)
                    if self.array_outer[i][0] == key:
                        inner_table = self.array_outer[i][1]
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
        :complexity: See _linear_probe.
        """
        index1, index2 = self._linear_probe(key[0], key[1], False)

        inner_table = self.array_outer[index1][1]
        return inner_table.array[index2][1] 
        

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        
        complexity: 
        - Best Case: O(hash1(key1) + hash2(key2)), when the first and second position is empty, and no rehashing is required.
        - Worst Case: O((hash1(key1) + N * comp(K1)) + (hash2(key2) + M * comp(K2)) + (N*hash(K) + N^2*comp(K)) + (N*hash(K) + N^2*comp(K))),
        Occurs when LinearProbing worst case happens and the outer and inner array has to rehash. 
        """
        # will create (k1, sub_table) if self.array_outer[index1] is None 
        # and increase self.count_outer automatically
        index1, index2 = self._linear_probe(key[0], key[1], True) 
        
        inner_table:LinearProbeTable = self.array_outer[index1][1]
        
        if inner_table.array[index2] is None:
            inner_table.count += 1
        
        inner_table.array[index2] = (key[1], data)
        
        if self.count_outer > self.table_size / 2:
            self._rehash()
        
        if inner_table.count > inner_table.table_size / 2:
            inner_table._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        complexity:
        - Best Case: O((hash1(key1) + hash2(key2)), Deletes a (key,value) pair and there are no gaps to fill.
        - Worst Case:O(((hash1(key1) + N * comp(K1)) + (hash2(key2) + M * comp(K2))) * (N + M)), deletes a (key,value) 
        pair and many gaps to fill
        """

        index1, index2 = self._linear_probe(key[0], key[1], False)

        inner_table = self.array_outer[index1][1]
        inner_table.array[index2] = None
        inner_table.count -= 1

        if inner_table.count == 0:
            self.array_outer[index1] = None
            self.count_outer -= 1
        
        index1 = (index1+1) % self.table_size
        while self.array_outer[index1] is not None:
            key1, inner_tabl = self.array_outer[index1]
            self.array_outer[index1] = None
            while inner_tabl.array[index2] is not None:
                key2, data = inner_tabl.array[index2]
                self[key1,key2] = data
                index2 = (index2+1) % inner_tabl.table_size
            index1 = (index1+1) % self.table_size


        

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array_outer
        self.size_index_outer += 1
        if self.size_index_outer == len(self.TABLE_SIZES):
            return
        self.array_outer = ArrayR(self.TABLE_SIZES[self.size_index_outer])
        self.count_outer = 0

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
        complexity:
        - O(1)
        - Best Case = Worst Case
        """
        return len(self.array_outer)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        complexity:
        - O(1)
        - Best case = Worst Case
        """
        return self.count_outer

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
    




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
        
        if sizes is not None:
            self.TABLE_SIZES = sizes
        
        self.internal_table = LinearProbeTable(internal_sizes)
        
        self.size_index_ = 0    # size_index for the outer table
        self.arrayO = ArrayR(self.TABLE_SIZES[self.size_index_]) # outer hash table
        self.counts = 0     # count for the outer table
       

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
        index1 = self.hash1(key1)
        sub_table:LinearProbeTable = None
        
        for i in range(self.table_size):    # self.table_size is the table size of the outer hash table
            if self.arrayO[index1] is None:     # if inner table does not exist
                top_lvl_keys = self.keys(None)
                if top_lvl_keys is None or key1 not in top_lvl_keys:
                    if is_insert:
                        sub_table = LinearProbeTable(self.internal_table.TABLE_SIZES)
                        self.arrayO[index1] = (key1, sub_table)
                        break
                    else:
                        raise KeyError(key1)
                
            elif self.arrayO[index1][0] == key1:
                sub_table = self.arrayO[index1][1]
                break
            else:
                if i == self.table_size-1:
                    raise FullError("Table is full!")
                index1 = (index1+1) % self.table_size
        
        index2 = self.hash2(key2, sub_table)
        for j in range(sub_table.table_size):
            if sub_table.array[index2] is None:
                bot_lvl_keys = self.keys(key1)
                if bot_lvl_keys is None or key2 not in bot_lvl_keys:
                    if is_insert:
                        sub_table.array[index2] = (key2, None)
                        break 
                    else:
                        raise KeyError(key2)
            elif sub_table.array[index2][0] == key2:
                break
            else:
                if j == sub_table.table_size-1:
                    raise FullError("Table is full!")
                index2 = (index2 + 1) % sub_table.table_size
        
        return index1, index2

            

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            top_lvl_keys = self.keys(None)
            iter_key = OurIterator(top_lvl_keys)
            try:
                item = next(iter_key)
                yield item
            except StopIteration:
                pass
        else:
            bot_lvl_keys = self.keys(key)
            iter_key = OurIterator(bot_lvl_keys)
            try:
                item = next(iter_key)      
                yield item          
            except StopIteration:
                pass

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """

        list_of_keys = []

        if key is None:
            for k1 in self.arrayO:
                if k1 is not None:
                    key1, value = k1
                    list_of_keys.append(key1)
        else:
            for item in self.arrayO:
                if item is not None:
                    ke1, val = item
                    if ke1 == key:
                        inner_table:LinearProbeTable = val
                        for k2 in inner_table.array:
                            if k2 is not None:
                                key2, data = k2
                                list_of_keys.append(key2)
        return list_of_keys



    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """

        if key is None:
            top_lvl_values = self.values(None)
            iter_val = OurIterator(top_lvl_values)
            try:
                item = next(iter_val)
                yield item
            except StopIteration:
                pass    
              
        else:
            bot_lvl_values = self.values(key)
            iter_val = OurIterator(bot_lvl_values)
            try:
                item = next(iter_val)
                yield item
            except StopIteration:
                pass
            

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """

        list_of_values = []

        if key is None:
            for item in self.arrayO:
                if item is not None:
                    k1, inner_table = item
                    for item1 in inner_table.array:
                        if item1 is not None:
                            key2, value = item1
                            list_of_values.append(value)
        else:
            for item2 in self.arrayO:
                if item2 is not None:
                    key1, inner_tabl = item2
                    if key == key1:
                        inner_tabl:LinearProbeTable
                        for item3 in inner_tabl.array:
                            if item3 is not None:
                                key3, val = item3
                                list_of_values.append(val)
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

        if self.arrayO[index1][0] == key[0]:
            inner_table:LinearProbeTable = self.arrayO[index1][1]
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
            self.counts += 1            

        indx1, indx2 = self._linear_probe(key[0], key[1], True)
        
        inner_table:LinearProbeTable = self.arrayO[indx1][1]
        if key[1] not in bot_lvl_keys:
            inner_table.count += 1

        inner_table.array[indx2] = (key[1], data)
        
        if self.counts > self.table_size / 2:
            self._rehash()
        
        if inner_table.count > inner_table.table_size / 2:
            inner_table._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """

        index1, index2 = self._linear_probe(key[0], key[1], False)

        inner_table:LinearProbeTable = self.arrayO[index1][1]
        inner_table.array[index2] = None
        inner_table.count -= 1

        if inner_table.count == 0:
            self.arrayO[index1] = None
            self.counts -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.arrayO
        self.size_index_ += 1
        if self.size_index_ == len(self.TABLE_SIZES):
            return
        self.arrayO = ArrayR(self.TABLE_SIZES[self.size_index_])
        self.counts = 0

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
        return len(self.arrayO)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.counts

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
    
    def is_full(self) -> bool:
        return self.counts == self.table_size
    
    def is_empty(self) -> bool:
        return self.counts == 0
    
class OurIterator:
    def __init__(self, iterable):
        self.iterator = iter(iterable)
    def __iter__(self):
        return self
    def __next__(self):
        data = next(self.iterator)
        if data is None:
            raise StopIteration
        return data

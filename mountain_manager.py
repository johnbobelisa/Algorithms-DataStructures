from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:
    
    DIFFICULTY_CHAR = '@'

    def __init__(self) -> None:
        """
         Complexity:
        - O(1): assuming DoubleKeyTable creation is O(1).
        - best case = worst case
        """
        self.manager_table = DoubleKeyTable()
        self.highest_difficulty = 0

    def add_mountain(self, mountain: Mountain):
        """
        Add a mountain to the manager
        
        Complexity:
        - O(comp): where comp is the time complexity of integer comparison and
        assuming DoubleKeyTable methods are O(1).
        - best case = worst case
        """
        key1 = mountain.difficulty_level * self.DIFFICULTY_CHAR
        self.manager_table[key1, mountain.name] = mountain      # O(1)
        if mountain.difficulty_level > self.highest_difficulty: # O(comp)
            self.highest_difficulty = mountain.difficulty_level

    def remove_mountain(self, mountain: Mountain):
        """
        Remove a mountain from the manager
        
        Complexity:
        - O(1): assuming DoubleKeyTable methods are O(1).
        - best case = worst case
        """
        key1 = mountain.difficulty_level * self.DIFFICULTY_CHAR
        del self.manager_table[key1, mountain.name]     # O(1)

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Remove the old mountain and add the new mountain.
        
        Complexity:
        See add_mountain and remove_mountain
        - O(comp): where comp is the time complexity of integer comparison and
        assuming DoubleKeyTable methods are O(1).
        - best case = worst case
        """
        self.remove_mountain(old)   # O(1)
        self.add_mountain(new)      # O(comp)

    def mountains_with_difficulty(self, diff: int):
        """
        Return a list of all mountains with this difficulty.
        
        Complexity:
        - O(1): assuming DoubleKeyTable methods are O(1).
        - best case = worst case
        """
        key1 = diff * self.DIFFICULTY_CHAR
        return self.manager_table.values(key1)      # O(1)

    def group_by_difficulty(self):
        """
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        
        Complexity:
        See mountains_with_difficulty
        - O(m): where m is the magnitude self.highest_difficulty
        - best case = worst case
        """
        all_mountains = []
        
        for i in range(self.highest_difficulty + 1):    # O(m)
            difficulty_list = self.mountains_with_difficulty(i)     # O(1)
            if difficulty_list:
                all_mountains.append(difficulty_list)
                
        return all_mountains
            

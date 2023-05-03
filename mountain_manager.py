from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:
    
    DIFFICULTY_CHAR = '@'

    def __init__(self) -> None:
        self.manager_table = DoubleKeyTable()
        self.highest_difficulty = 0

    def add_mountain(self, mountain: Mountain):
        """
        Add a mountain to the manager
        """
        key1 = mountain.difficulty_level * self.DIFFICULTY_CHAR
        self.manager_table[key1, mountain.name] = mountain
        if mountain.difficulty_level > self.highest_difficulty:
            self.highest_difficulty = mountain.difficulty_level

    def remove_mountain(self, mountain: Mountain):
        """
        Remove a mountain from the manager
        """
        key1 = mountain.difficulty_level * self.DIFFICULTY_CHAR
        del self.manager_table[key1, mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Remove the old mountain and add the new mountain.
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        """
        Return a list of all mountains with this difficulty.
        """
        key1 = diff * self.DIFFICULTY_CHAR
        return self.manager_table.values(key1)

    def group_by_difficulty(self):
        """
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        """
        all_mountains = []
        
        for i in range(self.highest_difficulty + 1):
            difficulty_list = self.mountains_with_difficulty(i)
            if difficulty_list:
                all_mountains.append(difficulty_list)
                
        return all_mountains
            

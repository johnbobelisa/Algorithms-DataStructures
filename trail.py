from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        self.path_top = Trail(None)
        self.path_bottom = Trail(None)
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        self.mountain = None
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None),Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, Trail(self.store)))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        current_store = self.store
        # following_stack stores path_follow Trail objects
        following_stack = LinkedStack()
        while current_store is not None or not following_stack.is_empty():
            # while loop ends when current_store is None and following_stack is empty
            if current_store.__class__.__name__ == "TrailSeries":
                personality.add_mountain(current_store.mountain)
                current_store = current_store.following.store
            elif current_store.__class__.__name__ == "TrailSplit":
                if personality.select_branch(current_store.path_top, current_store.path_bottom):
                    # top branch selected
                    following_stack.push(current_store.path_follow)
                    current_store = current_store.path_top.store
                else:
                    # bottom branch selected
                    following_stack.push(current_store.path_follow)
                    current_store = current_store.path_bottom.store
            else:   
                # current_store is None
                current_store = following_stack.pop().store
                
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
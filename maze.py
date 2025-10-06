"""
Maze class for managing maze layout and collision detection.
"""

import pygame
from config import (
    TILE_WALL, TILE_PATH, TILE_PLAYER_START, TILE_EXIT,
    TILE_OBSTACLE, TILE_COLLECTIBLE, CELL_SIZE
)

class Maze:
    """Manages the maze layout and game objects."""
    
    def __init__(self, layout, obstacles=None, collectibles=None):
        """
        Initialize maze.
        Args:
            layout: 2D list of characters representing maze
            obstacles: List of moving obstacle positions (optional)
            collectibles: List of collectible positions (optional)
        """
        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0]) if layout else 0
        self.obstacles = obstacles or []
        self.collectibles = collectibles or []
        self.collected = set()
        
        # Find player start and exit positions
        self.start_pos = None
        self.exit_pos = None
        self._find_special_tiles()
    
    def _find_special_tiles(self):
        """Find player start and exit positions in the maze."""
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == TILE_PLAYER_START:
                    self.start_pos = (x, y)
                elif tile == TILE_EXIT:
                    self.exit_pos = (x, y)
    
    def is_walkable(self, x, y):
        """Check if a position is walkable."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.layout[y][x] != TILE_WALL
    
    def is_exit(self, x, y):
        """Check if position is the exit."""
        return (x, y) == self.exit_pos
    
    def collect_item(self, x, y):
        """Try to collect an item at position."""
        pos = (x, y)
        if pos in self.collectibles and pos not in self.collected:
            self.collected.add(pos)
            return True
        return False
    
    def get_tile(self, x, y):
        """Get tile type at position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.layout[y][x]
        return TILE_WALL
    
    def update_obstacles(self, dt):
        """Update moving obstacles (for future enhancements)."""
        # Placeholder for moving obstacles logic
        pass
    
    def check_obstacle_collision(self, player_rect):
        """Check if player collides with any obstacles."""
        for obs_x, obs_y in self.obstacles:
            obs_rect = pygame.Rect(
                obs_x * CELL_SIZE,
                obs_y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            if player_rect.colliderect(obs_rect):
                return True
        return False
    
    def get_remaining_collectibles(self):
        """Get number of collectibles not yet collected."""
        return len(self.collectibles) - len(self.collected)
    
    def reset_collectibles(self):
        """Reset collected items."""
        self.collected.clear()

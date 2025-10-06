"""
Player class for the maze game.
"""

import pygame
from config import COLOR_PLAYER, CELL_SIZE, PLAYER_SPEED

class Player:
    """Represents the player in the maze."""
    
    def __init__(self, x, y):
        """
        Initialize player.
        Args:
            x: Grid x position
            y: Grid y position
        """
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.collectibles = 0
        self.score = 0
    
    def set_target(self, grid_x, grid_y):
        """Set target position for smooth movement."""
        self.target_x = grid_x * CELL_SIZE
        self.target_y = grid_y * CELL_SIZE
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.moving = True
    
    def update(self, dt):
        """Update player position with smooth movement."""
        if self.moving:
            # Move towards target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            # Calculate distance to move this frame
            move_distance = PLAYER_SPEED
            
            if abs(dx) <= move_distance and abs(dy) <= move_distance:
                # Reached target
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
            else:
                # Move towards target
                if dx != 0:
                    self.x += move_distance if dx > 0 else -move_distance
                if dy != 0:
                    self.y += move_distance if dy > 0 else -move_distance
    
    def get_rect(self):
        """Get player rectangle for collision detection."""
        margin = CELL_SIZE // 4
        return pygame.Rect(
            self.x + margin,
            self.y + margin,
            CELL_SIZE - margin * 2,
            CELL_SIZE - margin * 2
        )
    
    def collect_item(self):
        """Collect a collectible item."""
        self.collectibles += 1
        self.score += 100
    
    def add_score(self, points):
        """Add points to score."""
        self.score += points
    
    def reset_position(self, x, y):
        """Reset player to starting position."""
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False

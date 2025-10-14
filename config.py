"""
Configuration settings for the maze game.
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
FPS = 60

# Game settings
PLAYER_SPEED = 5
OBSTACLE_SPEED = 2
INITIAL_LIVES = 3
TIME_BONUS_MULTIPLIER = 10

# Tile types
TILE_WALL = 'W'
TILE_PATH = ' '
TILE_PLAYER_START = 'P'
TILE_EXIT = 'E'
TILE_OBSTACLE = 'O'
TILE_COLLECTIBLE = 'C'

# Files
SCORES_FILE = 'high_scores.json'
PROFILES_FILE = 'profiles.json'

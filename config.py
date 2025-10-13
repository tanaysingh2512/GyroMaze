"""
Configuration settings for the maze game.
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
FPS = 60

# Colors (RGB)
COLOR_WALL = (40, 40, 40)
COLOR_PATH = (240, 240, 240)
COLOR_PLAYER = (50, 150, 255)
COLOR_EXIT = (50, 255, 50)
COLOR_OBSTACLE = (255, 50, 50)
COLOR_COLLECTIBLE = (255, 215, 0)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_MENU_BG = (20, 20, 20)

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

# === Input selection & Sense HAT tuning ===
# Choose "sensehat" for tilt controls, "keyboard" to revert.
INPUT_METHOD = "sensehat"

# Tilt deadzone (degrees): ignore tiny hand shakes
GYRO_DEADZONE_DEG = 8.0

# EMA smoothing factor (0..1): higher = snappier, lower = smoother
GYRO_SMOOTH = 0.25

# Shake gesture -> acts like ENTER (confirm/next)
SHAKE_G_THRESHOLD = 1.7     # peak |accel| in g to count as a shake
SHAKE_DEBOUNCE_MS = 800     # min ms between shake-confirms



"""
Level definitions for the maze game.
10 progressively harder levels with different layouts and challenges.
"""

from config import TILE_WALL as W, TILE_PATH as _, TILE_PLAYER_START as P, TILE_EXIT as E

class LevelData:
    """Container for level information."""
    
    def __init__(self, number, layout, obstacles=None, collectibles=None, time_limit=None):
        self.number = number
        self.layout = layout
        self.obstacles = obstacles or []
        self.collectibles = collectibles or []
        self.time_limit = time_limit  # Optional time limit in seconds

# Level 1: Simple introduction maze
LEVEL_1 = LevelData(
    number=1,
    layout=[
        [W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, W, _, _, _, _, W],
        [W, _, W, _, W, _, W, W, _, W],
        [W, _, W, _, _, _, W, _, _, W],
        [W, _, W, W, W, _, W, _, W, W],
        [W, _, _, _, _, _, W, _, _, W],
        [W, W, W, W, W, _, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, W],
        [W, _, W, W, W, W, W, W, E, W],
        [W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(3, 3), (7, 5)],
    time_limit=60
)

# Level 2: Slightly larger with more turns
LEVEL_2 = LevelData(
    number=2,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, W, _, _, _, W, _, _, _, W],
        [W, _, _, W, _, W, _, W, _, W, _, W],
        [W, W, _, W, _, W, _, _, _, W, _, W],
        [W, _, _, _, _, W, W, W, W, W, _, W],
        [W, _, W, W, _, _, _, _, _, _, _, W],
        [W, _, W, _, _, W, W, W, W, W, _, W],
        [W, _, _, _, W, W, _, _, _, W, _, W],
        [W, W, W, _, _, _, _, W, _, _, _, W],
        [W, _, _, _, W, W, _, W, W, W, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(4, 2), (6, 5), (9, 7)],
    time_limit=90
)

# Level 3: Narrow passages
LEVEL_3 = LevelData(
    number=3,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, _, W, _, _, _, W, _, _, W],
        [W, W, W, W, _, W, _, W, _, W, _, W, W],
        [W, _, _, _, _, W, _, W, _, _, _, _, W],
        [W, _, W, W, W, W, _, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, W, _, W],
        [W, W, W, W, W, W, _, W, W, _, W, _, W],
        [W, _, _, _, _, _, _, W, _, _, W, _, W],
        [W, _, W, W, W, W, W, W, _, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(5, 3), (10, 5), (6, 8)],
    obstacles=[(6, 6)],
    time_limit=100
)

# Level 4: Multiple paths
LEVEL_4 = LevelData(
    number=4,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, W, _, _, _, W, _, _, _, _, W],
        [W, _, W, _, W, _, W, _, W, _, W, W, _, W],
        [W, _, W, _, _, _, W, _, _, _, W, _, _, W],
        [W, _, W, W, W, W, W, _, W, _, W, _, W, W],
        [W, _, _, _, _, _, _, _, W, _, _, _, _, W],
        [W, W, W, _, W, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, W, _, W],
        [W, _, W, W, W, W, W, W, _, W, _, W, _, W],
        [W, _, _, _, _, _, _, _, _, W, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(3, 2), (7, 4), (11, 6), (5, 8)],
    obstacles=[(6, 5)],
    time_limit=110
)

# Level 5: Spiral maze
LEVEL_5 = LevelData(
    number=5,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, _, W, W, W, W, W, W, W, W, W, W, W, _, W],
        [W, _, W, _, _, _, _, _, _, _, _, _, W, _, W],
        [W, _, W, _, W, W, W, W, W, W, W, _, W, _, W],
        [W, _, W, _, _, _, _, _, _, _, W, _, W, _, W],
        [W, _, W, _, W, _, W, W, W, _, W, _, W, _, W],
        [W, _, W, _, W, _, W, E, _, _, W, _, W, _, W],
        [W, _, W, _, W, _, W, W, W, _, W, _, W, _, W],
        [W, _, W, _, W, _, _, _, _, _, W, _, W, _, W],
        [W, _, W, _, W, W, W, W, W, W, W, _, W, _, W],
        [W, _, W, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, _, W, W, W, W, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(7, 3), (7, 9), (11, 6), (3, 11)],
    obstacles=[(7, 5), (9, 10)],
    time_limit=120
)

# Level 6: Dense maze
LEVEL_6 = LevelData(
    number=6,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, W, _, _, _, W, _, _, _, W, _, _, W],
        [W, W, _, W, _, W, _, W, _, W, _, W, _, W, W],
        [W, _, _, W, _, W, _, _, _, W, _, _, _, W, W],
        [W, _, W, W, _, W, W, W, W, W, W, W, _, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, W, _, W, W],
        [W, W, W, _, W, W, W, _, W, W, _, W, _, _, W],
        [W, _, _, _, W, _, _, _, W, _, _, W, W, _, W],
        [W, _, W, W, W, _, W, _, W, _, W, _, _, _, W],
        [W, _, _, _, _, _, W, _, _, _, W, _, W, W, W],
        [W, W, W, W, W, _, W, W, W, _, W, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(4, 2), (8, 4), (11, 6), (5, 8), (2, 9)],
    obstacles=[(6, 5), (10, 8)],
    time_limit=130
)

# Level 7: Long corridors
LEVEL_7 = LevelData(
    number=7,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, _, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, _, W],
        [W, _, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(7, 1), (14, 3), (7, 5), (14, 7), (7, 9)],
    obstacles=[(5, 2), (15, 5), (0, 7)],
    time_limit=140
)

# Level 8: Zigzag maze
LEVEL_8 = LevelData(
    number=8,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, _, W, _, _, _, _, _, W, _, _, _, W],
        [W, W, W, W, _, W, _, W, W, W, _, W, _, W, W, W],
        [W, _, _, _, _, W, _, W, _, _, _, W, _, _, _, W],
        [W, _, W, W, W, W, _, W, _, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, W, _, _, _, _, _, W, _, W],
        [W, W, W, W, W, W, _, W, W, W, W, W, _, W, _, W],
        [W, _, _, _, _, W, _, _, _, _, _, W, _, W, _, W],
        [W, _, W, W, _, W, W, W, W, W, _, W, _, W, _, W],
        [W, _, W, _, _, _, _, _, _, _, _, _, _, W, _, W],
        [W, _, W, _, W, W, W, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, _, _, _, _, _, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(3, 2), (8, 4), (11, 6), (4, 9), (13, 10)],
    obstacles=[(7, 3), (10, 7), (6, 10)],
    time_limit=150
)

# Level 9: Complex branching
LEVEL_9 = LevelData(
    number=9,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, W, _, _, _, W, _, _, _, W, _, _, _, _, W],
        [W, _, _, W, _, W, _, W, _, W, _, W, _, W, W, _, W],
        [W, W, _, W, _, W, _, _, _, W, _, _, _, W, _, _, W],
        [W, _, _, W, _, W, W, W, W, W, W, W, _, W, _, W, W],
        [W, _, W, W, _, _, _, _, _, _, _, W, _, _, _, _, W],
        [W, _, _, _, _, W, W, W, W, W, _, W, W, W, W, _, W],
        [W, W, W, W, _, W, _, _, _, W, _, _, _, _, W, _, W],
        [W, _, _, _, _, W, _, W, _, W, W, W, W, _, W, _, W],
        [W, _, W, W, W, W, _, W, _, _, _, _, W, _, W, _, W],
        [W, _, _, _, _, _, _, W, W, W, W, _, W, _, _, _, W],
        [W, W, W, W, W, W, _, _, _, _, W, _, W, W, W, _, W],
        [W, _, _, _, _, _, _, W, W, _, W, _, _, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(4, 2), (9, 3), (13, 5), (6, 8), (11, 10), (4, 11)],
    obstacles=[(8, 4), (12, 7), (6, 10)],
    time_limit=160
)

# Level 10: Ultimate challenge
LEVEL_10 = LevelData(
    number=10,
    layout=[
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [W, P, _, _, _, W, _, _, _, _, _, W, _, _, _, W, _, W],
        [W, W, W, W, _, W, _, W, W, W, _, W, _, W, _, W, _, W],
        [W, _, _, _, _, W, _, W, _, _, _, _, _, W, _, _, _, W],
        [W, _, W, W, W, W, _, W, _, W, W, W, W, W, W, W, _, W],
        [W, _, _, _, _, _, _, W, _, _, _, _, _, _, _, W, _, W],
        [W, W, W, _, W, W, W, W, W, W, W, W, W, W, _, W, _, W],
        [W, _, _, _, W, _, _, _, _, _, _, _, _, W, _, W, _, W],
        [W, _, W, W, W, _, W, W, W, W, W, W, _, W, _, W, _, W],
        [W, _, _, _, _, _, W, _, _, _, _, W, _, _, _, W, _, W],
        [W, W, W, W, W, _, W, _, W, W, _, W, W, W, W, W, _, W],
        [W, _, _, _, W, _, _, _, W, _, _, _, _, _, _, _, _, W],
        [W, _, W, _, W, W, W, W, W, _, W, W, W, W, W, W, W, W],
        [W, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _, E, W],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    ],
    collectibles=[(3, 2), (8, 3), (13, 4), (5, 7), (11, 8), (4, 11), (14, 12)],
    obstacles=[(9, 4), (6, 7), (13, 9), (7, 11)],
    time_limit=180
)

# List of all levels
ALL_LEVELS = [
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5,
    LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10
]

def get_level(level_number):
    """Get level data by level number (1-10)."""
    if 1 <= level_number <= 10:
        return ALL_LEVELS[level_number - 1]
    return None

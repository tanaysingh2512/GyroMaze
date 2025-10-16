PALETTES = {
    'DEFAULT': {
        "COLOR_WALL": (40, 40, 40),
        "COLOR_PATH": (200, 200, 200),
        "COLOR_PLAYER": (50, 150, 255),   # Bright Blue
        "COLOR_EXIT": (50, 255, 50),      # Bright Green
        "COLOR_OBSTACLE": (255, 50, 50),  # Bright Red
        "COLOR_COLLECTIBLE": (255, 215, 0), # Gold
        "COLOR_BACKGROUND": (30, 30, 30),
        "COLOR_TEXT": (255, 255, 255),
        "COLOR_MENU_BG": (20, 20, 20),
        "COLOR_WALL_BORDER": (60, 60, 60),
        "COLOR_MENU_SELECTED": (255, 255, 100), # Yellow highlight
        "COLOR_VICTORY_TITLE": (255, 215, 0)
    },

    'TRITANOPIA': {
        "COLOR_WALL": (70, 60, 90),       # Dark Purple-Gray
        "COLOR_PATH": (210, 200, 220),    # Light Lavender
        "COLOR_PLAYER": (255, 0, 255),    # Bright Magenta
        "COLOR_EXIT": (0, 255, 255),      # Bright Cyan
        "COLOR_OBSTACLE": (255, 105, 180),# Hot Pink
        "COLOR_COLLECTIBLE": (255, 255, 0), # Yellow
        "COLOR_BACKGROUND": (40, 30, 50), # Deep Purple
        "COLOR_TEXT": (255, 255, 255),
        "COLOR_MENU_BG": (25, 20, 35),    # Very Dark Purple
        "COLOR_WALL_BORDER": (100, 90, 120),
        "COLOR_MENU_SELECTED": (0, 255, 255), # Cyan highlight
        "COLOR_VICTORY_TITLE": (255, 255, 0)
    },

    'DEUTERANOPIA': {
        "COLOR_WALL": (80, 60, 45),       # Dark Brown
        "COLOR_PATH": (250, 245, 225),    # Cream
        "COLOR_PLAYER": (0, 114, 178),    # Strong Blue
        "COLOR_EXIT": (86, 180, 233),     # Sky Blue
        "COLOR_OBSTACLE": (210, 90, 0),   # Burnt Orange
        "COLOR_COLLECTIBLE": (230, 159, 0), # Orange
        "COLOR_BACKGROUND": (250, 245, 225), # Cream
        "COLOR_TEXT": (50, 40, 30),       # Dark Brown Text
        "COLOR_MENU_BG": (245, 240, 220), # Light Cream
        "COLOR_WALL_BORDER": (120, 100, 85),
        "COLOR_MENU_SELECTED": (0, 114, 178), # Blue highlight
        "COLOR_VICTORY_TITLE": (210, 90, 0)
    },

    'PROTANOPIA': {
        "COLOR_WALL": (25, 70, 85),       # Dark Teal
        "COLOR_PATH": (140, 160, 170),    # Light Blue-Gray
        "COLOR_PLAYER": (240, 228, 66),    # Bright Yellow
        "COLOR_EXIT": (86, 180, 233),     # Sky Blue
        "COLOR_OBSTACLE": (230, 230, 230), # White
        "COLOR_COLLECTIBLE": (255, 170, 50), # Light Orange
        "COLOR_BACKGROUND": (15, 40, 55), # Deep Blue/Teal
        "COLOR_TEXT": (255, 255, 255),
        "COLOR_MENU_BG": (10, 25, 35),    # Very Dark Teal
        "COLOR_WALL_BORDER": (45, 100, 115),
        "COLOR_MENU_SELECTED": (240, 228, 66), # Yellow highlight
        "COLOR_VICTORY_TITLE": (240, 228, 66)
    }
}

CURRENT_PALETTE = PALETTES['DEFAULT'].copy()

def set_palette(name):
  """Sets the global current color palette."""
  global CURRENT_PALETTE
  palette = PALETTES.get(name)
  if palette:
      CURRENT_PALETTE = palette.copy()

def get_color(name: str):
    """
    Gets a specific color from the current palette.
    Raises a KeyError if the color name is not found.
    """
    color = CURRENT_PALETTE.get(name)
    if color is None:
        raise KeyError(f"Color '{name}' not found in the current palette.")
    return color

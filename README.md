# Maze Game

A lightweight Python maze game with 10 progressively challenging levels. Control your character using keyboard input (arrow keys or WASD) and navigate through increasingly complex mazes!

## Features

- 🎮 **10 Progressive Levels**: Each level increases in difficulty with larger mazes and more obstacles
- ⌨️ **Keyboard Controls**: Use arrow keys or WASD for movement
- 🏆 **High Score System**: Track your best scores and compete with yourself
- 👤 **Player Profiles**: Create profiles with just your name
- ⭐ **Collectibles**: Gather bonus items for extra points
- ⏱️ **Time Challenges**: Beat the clock to earn time bonuses
- 💛 **Lives System**: Start with 3 lives - use them wisely!
- 🎯 **Obstacles**: Avoid red obstacles in later levels

## Modular Design for Raspberry Pi

The game is built with a modular input system that makes it easy to switch from keyboard to gyroscopic sensor control:

- **Abstract Input Handler**: The `input_handler.py` module uses an abstract base class
- **Easy Switching**: Simply swap `KeyboardInputHandler` with `GyroscopeInputHandler` in `game_manager.py`
- **Placeholder Included**: A `GyroscopeInputHandler` class is already scaffolded for your sensor implementation

### To Add Gyroscope Support

1. Install your gyroscope library (e.g., `mpu6050-raspberrypi`)
2. Implement the sensor reading logic in `input_handler.py` → `GyroscopeInputHandler.update()`
3. Change this line in `game_manager.py`:
   ```python
   # From:
   self.input_handler = KeyboardInputHandler()
   # To:
   self.input_handler = GyroscopeInputHandler()
   ```

## Installation

### Requirements

- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download this repository**

2. **Navigate to the game directory**
   ```bash
   cd "maze game"
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install pygame directly:
   ```bash
   pip install pygame
   ```

## How to Play

### Starting the Game

Run the game with:
```bash
python main.py
```

### Controls

- **Arrow Keys** or **WASD**: Move your character (blue square)
- **ESC**: Return to main menu
- **Enter**: Confirm selections

### Game Elements

- 🟦 **Blue Square**: Your player
- ⬜ **White/Gray Tiles**: Walkable paths
- ⬛ **Black Tiles**: Walls (can't pass through)
- 🟩 **Green Tile**: Exit (reach it to complete the level)
- 🟡 **Yellow Circles**: Collectibles (100 points each)
- 🟥 **Red Squares**: Obstacles (lose a life if touched)

### Scoring

- **Collectibles**: 100 points each
- **Level Completion Bonus**: 50 points per collectible gathered
- **Time Bonus**: Points for finishing before time runs out (varies by level)

### Lives

- Start with 3 lives
- Lose a life when:
  - You touch an obstacle
  - Time runs out on a level
- When you lose a life, the level resets
- Game over when all lives are lost

## Game Structure

```
maze game/
├── main.py                 # Entry point - runs the game
├── config.py              # Game settings and constants
├── game_manager.py        # Game state and flow coordination
├── input_handler.py       # Input handling (keyboard/gyroscope)
├── maze.py                # Maze logic and collision detection
├── player.py              # Player character logic
├── renderer.py            # Graphics rendering
├── levels.py              # All 10 level definitions
├── profile_manager.py     # Profile and high score management
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── high_scores.json      # Generated: High scores data
└── profiles.json         # Generated: Player profiles data
```

## Level Progression

1. **Level 1**: Simple introduction maze
2. **Level 2**: Larger with more turns
3. **Level 3**: Narrow passages + first obstacle
4. **Level 4**: Multiple paths to choose
5. **Level 5**: Spiral design with multiple obstacles
6. **Level 6**: Dense maze with more obstacles
7. **Level 7**: Long corridors with strategic obstacles
8. **Level 8**: Zigzag patterns
9. **Level 9**: Complex branching paths
10. **Level 10**: Ultimate challenge!

Each level has:
- Increasing maze complexity
- More collectibles to find
- Additional obstacles (starting from level 3)
- Longer time limits

## Customization

### Changing Colors

Edit `config.py` to customize colors:
```python
COLOR_PLAYER = (50, 150, 255)  # Blue
COLOR_WALL = (40, 40, 40)      # Dark gray
# ... and more
```

### Adjusting Difficulty

In `config.py`, modify:
```python
INITIAL_LIVES = 3           # Starting lives
PLAYER_SPEED = 5            # Movement speed
TIME_BONUS_MULTIPLIER = 10  # Time bonus calculation
```

### Creating Custom Levels

Add new levels in `levels.py`. Use these symbols:
- `W`: Wall
- `_`: Path (space)
- `P`: Player start position
- `E`: Exit
- Collectibles and obstacles are defined separately in lists

## Troubleshooting

### Pygame not found
```bash
pip install --upgrade pygame
```

### Game runs slowly
- Reduce FPS in `config.py` (default is 60)
- Make sure you're using a recent Python version

### Controls not responding
- Make sure the game window has focus
- Try clicking on the game window

## For Raspberry Pi

When running on Raspberry Pi:

1. **Install pygame**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pygame
   ```

2. **For gyroscope integration**, install your sensor library:
   ```bash
   pip install mpu6050-raspberrypi
   # or your specific sensor library
   ```

3. **Run with Python 3**:
   ```bash
   python3 main.py
   ```

## Credits

Created as a modular, educational maze game designed for easy hardware integration.

## License

Free to use and modify. Have fun! 🎮

---

**Enjoy the game!** Try to beat all 10 levels and get the highest score! 🏆

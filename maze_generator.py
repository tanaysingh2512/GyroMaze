import random
from collections import deque
from levels import LevelData, get_level, ALL_LEVELS
from config import TILE_WALL as W, TILE_PATH as PATH, TILE_PLAYER_START as P, TILE_EXIT as E, TILE_OBSTACLE as O, TILE_COLLECTIBLE as C

class MazeGenerator:
    def __init__(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height

        self.cell_width = (width - 1) // 2
        self.cell_height = (height - 1) // 2

        self.parent = {}
        self.rank = {}

    def _initialize_dsu(self):
        for r in range(self.cell_height):
            for c in range(self.cell_width):
                cell = (r, c)
                self.parent[cell] = cell
                self.rank[cell] = 0

    def _find_set(self, cell):
        if self.parent[cell] == cell:
            return cell
        self.parent[cell] = self._find_set(self.parent[cell])
        return self.parent[cell]

    def _unite_sets(self, cell1, cell2):
        root1 = self._find_set(cell1) 
        root2 = self._find_set(cell2)
        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                root1, root2 = root2, root1
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1
            return True
        return False

    def generate(self, loop_probability=0.25):
        self._initialize_dsu()

        layout = [[W for _ in range(self.width)] for _ in range(self.height)]

        # Create a list of all interior walls
        walls = []
        for r in range(self.cell_height):
            for c in range(self.cell_width):
                if r < self.cell_height - 1: walls.append(((r, c), (r + 1, c)))
                if c < self.cell_width - 1: walls.append(((r, c), (r, c + 1)))

        random.shuffle(walls)

        # Phase 1: Create initial perfect maze
        remaining_walls = []
        for cell1, cell2 in walls:
            if self._unite_sets(cell1, cell2):
                layout[2 * cell1[0] + 1][2 * cell1[1] + 1] = PATH
                layout[2 * cell2[0] + 1][2 * cell2[1] + 1] = PATH
                wall_r = cell1[0] + cell2[0] + 1
                wall_c = cell1[1] + cell2[1] + 1
                layout[wall_r][wall_c] = PATH
            else:
                # This wall would create a loop, save it for later
                remaining_walls.append((cell1, cell2))

        # Phase 2: Add loops for complexity by removing some remaining walls
        num_loops_to_create = int(len(remaining_walls) * loop_probability)
        for _ in range(num_loops_to_create):
            if not remaining_walls:
                break
            cell1, cell2 = remaining_walls.pop(random.randrange(len(remaining_walls)))
            wall_r = cell1[0] + cell2[0] + 1
            wall_c = cell1[1] + cell2[1] + 1
            layout[wall_r][wall_c] = PATH

        return layout

def _find_reachable_nodes(layout, start_pos, obstacles=[]):
    width, height = len(layout[0]), len(layout)
    queue = deque([start_pos])
    visited = {start_pos}
    obstacle_set = set(obstacles)

    while queue:
        x, y = queue.popleft()

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                # Check if the new position is valid and not visited
                if (nx, ny) not in visited and \
                   layout[ny][nx] != W and \
                   (nx, ny) not in obstacle_set:

                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return visited

def create_randomized_level(level_number):
    if not (1 <= level_number <= len(ALL_LEVELS)):
        return None

    original_level = get_level(level_number)
    if not original_level:
        return None

    height = len(original_level.layout)
    width = len(original_level.layout[0])

    generator = MazeGenerator(width, height)
    layout = generator.generate()

    path_coords = []
    for r_idx, row in enumerate(layout):
        for c_idx, tile in enumerate(row):
            if tile == PATH:
                path_coords.append((c_idx, r_idx))

    if not path_coords:
        return None # Failsafe

    # Place Player (P) near top-left and Exit (E) near bottom-right
    player_pos = path_coords[0]
    layout[player_pos[1]][player_pos[0]] = P
    path_coords.pop(0)

    exit_pos = path_coords[-1]
    layout[exit_pos[1]][exit_pos[0]] = E
    path_coords.pop(-1)

    random.shuffle(path_coords)

    # Determine number of items based on level number
    num_collectibles = 1 + level_number // 2
    num_obstacles = level_number // 3

    # 1. Place Obstacles Strategically
    obstacles = []
    possible_obstacle_locs = path_coords[:]

    for _ in range(num_obstacles):
        if not possible_obstacle_locs: break

        for _ in range(len(possible_obstacle_locs)):
            pos = possible_obstacle_locs.pop(0)

            temp_obstacles = obstacles + [pos]
            reachable_after_block = _find_reachable_nodes(layout, player_pos, temp_obstacles)

            if exit_pos in reachable_after_block:
                obstacles.append(pos)
                break
            else:
                possible_obstacle_locs.append(pos)

    # 2. Place Collectibles in Guaranteed Reachable Locations
    collectibles = []

    all_reachable_nodes = _find_reachable_nodes(layout, player_pos, obstacles)

    valid_collectible_locs = [
        pos for pos in all_reachable_nodes
        if pos != player_pos and pos != exit_pos and pos not in obstacles
    ]
    random.shuffle(valid_collectible_locs)

    # Place the desired number of collectibles
    for i in range(min(num_collectibles, len(valid_collectible_locs))):
        collectibles.append(valid_collectible_locs[i])

    # Create the final LevelData object
    random_level = LevelData(
        number=level_number,
        layout=layout,
        collectibles=collectibles,
        obstacles=obstacles,
        time_limit=original_level.time_limit
    )

    return random_level

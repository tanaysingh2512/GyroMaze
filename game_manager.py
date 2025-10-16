"""
Game manager - coordinates all game logic and state.
"""

import pygame
from enum import Enum

from maze import Maze
from player import Player
from renderer import Renderer
from input_handler import KeyboardInputHandler, SenseHatGyroInputHandler
from profile_manager import ProfileManager
from maze_generator import create_randomized_level
from levels import ALL_LEVELS
from config import (
    INPUT_METHOD,
    GYRO_DEADZONE_DEG,
    GYRO_SMOOTH,
    SHAKE_G_THRESHOLD,
    SHAKE_DEBOUNCE_MS,
    INITIAL_LIVES,
    TIME_BONUS_MULTIPLIER,
)
import color_manager

class GameState(Enum):
    """Game states."""
    MENU = 1
    PROFILE_SELECT = 2
    PROFILE_CREATE = 3
    PLAYING = 4
    PAUSED = 5
    LEVEL_COMPLETE = 6
    GAME_OVER = 7
    VICTORY = 8
    HIGH_SCORES = 9
    OPTIONS = 10


class GameManager:
    """Manages overall game state and flow."""
    def __init__(self, screen):
        self.screen = screen
        self.renderer = Renderer(screen)
        self.profile_manager = ProfileManager()

        # Input selection
        if str(INPUT_METHOD).lower() == "sensehat":
            self.input_handler = SenseHatGyroInputHandler(
                deadzone_deg=GYRO_DEADZONE_DEG,
                smooth=GYRO_SMOOTH,
                shake_g_threshold=SHAKE_G_THRESHOLD,
                shake_debounce_ms=SHAKE_DEBOUNCE_MS,
            )
        else:
            self.input_handler = KeyboardInputHandler()

        # Game state
        self.state = GameState.MENU
        self.current_level = 1
        self.lives = INITIAL_LIVES
        self.total_score = 0

        # Game objects
        self.maze: Maze | None = None
        self.player: Player | None = None

        # Timing
        self.level_time = 0.0
        self.time_limit = None

        # Menu
        self.menu_options = ["New Game", "High Scores", "Options", "Quit"]
        self.menu_selected = 0

        # Profile creation / selection
        self.options_menu = {
            "Default": "DEFAULT",
            "Purple (Tritanopia)": "TRITANOPIA",
            "Yellow (Deuteranopia)": "DEUTERANOPIA",
            "Yellow (Protanopia)": "PROTANOPIA",
            "Back": None
        }
        self.options_keys = list(self.options_menu.keys())
        self.options_selected = 0
        
        # Profile creation
        self.profile_input = ""
        self.profile_list = []
        self.profile_selected = 0

        # Message display
        self.message = None
        self.message_timer = 0.0

    # ------------------- Main loop integration -------------------

    def update(self, events, dt):
        """Update game state."""
        if self.state == GameState.MENU:
            return self._update_menu(events)
        elif self.state == GameState.PROFILE_SELECT:
            return self._update_profile_select(events)
        elif self.state == GameState.PROFILE_CREATE:
            return self._update_profile_create(events)
        elif self.state == GameState.OPTIONS:
            return self._update_options(events)
        elif self.state == GameState.PLAYING:
            return self._update_playing(events, dt)
        elif self.state == GameState.LEVEL_COMPLETE:
            return self._update_level_complete(events)
        elif self.state == GameState.GAME_OVER:
            return self._update_game_over(events)
        elif self.state == GameState.VICTORY:
            return self._update_victory(events)
        elif self.state == GameState.HIGH_SCORES:
            return self._update_high_scores(events)
        return True

    def _update_options(self, events):
        """Update options menu."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.options_selected = (self.options_selected - 1) % len(self.options_keys)
                elif event.key == pygame.K_DOWN:
                    self.options_selected = (self.options_selected + 1) % len(self.options_keys)
                elif event.key == pygame.K_RETURN:
                    selected_option_key = self.options_keys[self.options_selected]
                    palette_name = self.options_menu[selected_option_key]
                    if palette_name:
                        color_manager.set_palette(palette_name)
                    self.state = GameState.MENU
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
        return True
    
    def render(self):
        """Render current game state."""
        self.renderer.clear()

        if self.state == GameState.MENU:
            self.renderer.render_menu("MAZE GAME", self.menu_options, self.menu_selected)

        elif self.state == GameState.PROFILE_SELECT:
            options = self.profile_list + ["Create New Profile", "Back"]
            title = "Select Profile"
            self.renderer.render_menu(title, options, self.profile_selected)

        elif self.state == GameState.PROFILE_CREATE:
            self.renderer.render_menu(
                "Create Profile",
                [f"Name: {self.profile_input}_", "Press ENTER to confirm", "ESC to cancel"],
                0,
            )

            self.renderer.render_menu("Create Profile", [f"Name: {self.profile_input}_", "Press ENTER to confirm", "ESC to cancel"], 0)

        elif self.state == GameState.OPTIONS:
         self.renderer.render_menu("Color Options", self.options_keys, self.options_selected)
        
        elif self.state == GameState.PLAYING:
            if self.maze and self.player:
                offset_x, offset_y = self.renderer.get_maze_offset(self.maze)
                self.renderer.render_maze(self.maze, offset_x, offset_y)
                self.renderer.render_player(self.player, offset_x, offset_y)

                # Calculate remaining time
                time_remaining = None
                if self.time_limit:
                    time_remaining = max(0, self.time_limit - self.level_time)

                self.renderer.render_hud(
                    self.current_level,
                    self.total_score,
                    self.player.collectibles,
                    time_remaining,
                    self.lives,
                )

                # Display transient messages
                if self.message and self.message_timer > 0:
                    self.renderer.render_message(self.message)

        elif self.state == GameState.LEVEL_COMPLETE:
            if self.maze and self.player:
                offset_x, offset_y = self.renderer.get_maze_offset(self.maze)
                self.renderer.render_maze(self.maze, offset_x, offset_y)
                self.renderer.render_player(self.player, offset_x, offset_y)
            self.renderer.render_message("LEVEL COMPLETE!", "Press ENTER to continue")

        elif self.state == GameState.GAME_OVER:
            self.renderer.render_game_over(self.total_score, self.current_level)

        elif self.state == GameState.VICTORY:
            self.renderer.render_victory(self.total_score)

        elif self.state == GameState.HIGH_SCORES:
            self._render_high_scores()

    # ------------------------- Helpers ---------------------------

    def _inject_gyro_confirm(self, events):
        """If using Sense HAT: a quick shake acts like pressing Enter."""
        if isinstance(self.input_handler, SenseHatGyroInputHandler) and self.input_handler.consume_confirm():
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

    # -------------------- State: Menu / Profiles -----------------

    def _update_menu(self, events):
        """Update main menu."""
        # Allow shake to act like Enter
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_selected == 0:  # New Game
                        self._show_profile_select()
                    elif self.menu_selected == 1:  # High Scores
                        self.state = GameState.HIGH_SCORES
                    elif self.menu_selected == 2:  # Options
                        self.state = GameState.OPTIONS
                    elif self.menu_selected == 3:  # Quit
                        return False
        return True

    def _show_profile_select(self):
        """Show profile selection screen."""
        self.profile_list = self.profile_manager.get_all_profiles()
        self.profile_selected = 0
        self.state = GameState.PROFILE_SELECT

    def _update_profile_select(self, events):
        """Update profile selection screen."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        options_count = len(self.profile_list) + 2  # profiles + create new + back
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.profile_selected = (self.profile_selected - 1) % options_count
                elif event.key == pygame.K_DOWN:
                    self.profile_selected = (self.profile_selected + 1) % options_count
                elif event.key == pygame.K_RETURN:
                    if self.profile_selected < len(self.profile_list):
                        # Select existing profile
                        profile_name = self.profile_list[self.profile_selected]
                        self.profile_manager.current_profile = profile_name
                        self._start_new_game()
                    elif self.profile_selected == len(self.profile_list):
                        # Create new profile
                        self.profile_input = ""
                        self.state = GameState.PROFILE_CREATE
                    else:
                        # Back
                        self.state = GameState.MENU
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
        return True

    def _update_profile_create(self, events):
        """Update profile creation screen."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.profile_manager.create_profile(self.profile_input):
                        self._start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self._show_profile_select()
                elif event.key == pygame.K_BACKSPACE:
                    self.profile_input = self.profile_input[:-1]
                elif event.unicode and event.unicode.isprintable() and len(self.profile_input) < 20:
                    self.profile_input += event.unicode
        return True

    # ----------------------- State: Playing ----------------------

    def _start_new_game(self):
        """Start a new game with current profile."""
        self.current_level = 1
        self.lives = INITIAL_LIVES
        self.total_score = 0
        self._load_level(1)
        self.state = GameState.PLAYING

    def _load_level(self, level_number):
        """Load a specific level."""
        level_data = create_randomized_level(level_number)
        if not level_data:
            self.state = GameState.VICTORY
            return

        self.maze = Maze(
            level_data.layout,
            level_data.obstacles,
            level_data.collectibles,
        )

        if self.maze.start_pos:
            self.player = Player(*self.maze.start_pos)

        self.level_time = 0.0
        self.time_limit = level_data.time_limit
        self.current_level = level_number

    def _update_playing(self, events, dt):
        """Update playing state."""
        # Pause/back to menu
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
                return True

        # Update input
        self.input_handler.update(events)

        # Update timer
        self.level_time += dt
        if self.time_limit and self.level_time >= self.time_limit:
            self._lose_life()
            return True

        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = None

        # Grid-stepping: only issue a new target when not already moving
        if self.player and self.maze and not self.player.moving:
            dx, dy = self.input_handler.get_direction()
            if dx != 0 or dy != 0:
                new_x = self.player.grid_x + dx
                new_y = self.player.grid_y + dy
                if self.maze.is_walkable(new_x, new_y):
                    self.player.set_target(new_x, new_y)

        # Update entities
        if self.player:
            self.player.update(dt)
        if self.maze:
            # Enable moving obstacle logic
            self.maze.update_obstacles(dt)

            # Collectibles
            if self.maze.collect_item(self.player.grid_x, self.player.grid_y):
                self.player.collect_item()
                self.total_score += 100

            # Exit
            if self.maze.is_exit(self.player.grid_x, self.player.grid_y):
                self._complete_level()

            # Obstacle collision
            if self.maze.check_obstacle_collision(self.player.get_rect()):
                self._lose_life()

        return True

    # ---------------- Level complete / Game over / Victory -------

    def _complete_level(self):
        """Handle level completion."""
        # Calculate bonuses
        time_bonus = 0
        if self.time_limit:
            time_remaining = max(0, self.time_limit - self.level_time)
            time_bonus = int(time_remaining * TIME_BONUS_MULTIPLIER)

        collectible_bonus = self.player.collectibles * 50 if self.player else 0
        self.total_score += time_bonus + collectible_bonus

        self.state = GameState.LEVEL_COMPLETE

    def _update_level_complete(self, events):
        """Update level complete state."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.current_level >= len(ALL_LEVELS):
                    # Game completed
                    self._end_game(victory=True)
                else:
                    # Next level
                    self._load_level(self.current_level + 1)
                    self.state = GameState.PLAYING
        return True

    def _lose_life(self):
        """Handle losing a life."""
        self.lives -= 1

        if self.lives <= 0:
            self._end_game(victory=False)
        else:
            # Reset level
            if self.player and self.maze and self.maze.start_pos:
                self.player.reset_position(*self.maze.start_pos)
            self.level_time = 0.0
            if self.maze:
                self.maze.reset_collectibles()
            if self.player:
                self.player.collectibles = 0
            self.message = "Life Lost!"
            self.message_timer = 2.0

    def _end_game(self, victory: bool):
        """End the game and update profiles/high scores."""
        profile_name = self.profile_manager.get_current_profile_name()
        if profile_name:
            self.profile_manager.update_profile(self.total_score, self.current_level)
            self.profile_manager.add_score(profile_name, self.total_score, self.current_level)

        self.state = GameState.VICTORY if victory else GameState.GAME_OVER

    def _update_game_over(self, events):
        """Update game over state."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = GameState.MENU
        return True

    def _update_victory(self, events):
        """Update victory state."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = GameState.MENU
        return True

    def _update_high_scores(self, events):
        """Update high scores display."""
        self.input_handler.update(events)
        self._inject_gyro_confirm(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.state = GameState.MENU
        return True

    # ---------------------- Render helpers -----------------------

    def _render_high_scores(self):
        """Render high scores screen."""
        from config import SCREEN_WIDTH
        
        self.screen.fill(color_manager.get_color("COLOR_MENU_BG"))
        
        # Title
        title_surf = self.renderer.font_large.render("HIGH SCORES", True, color_manager.get_color("COLOR_TEXT"))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Scores
        scores = self.profile_manager.get_high_scores()
        y_pos = 150

        if not scores:
            no_scores = self.renderer.font_medium.render("No high scores yet!", True, color_manager.get_color("COLOR_TEXT"))
            no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            for i, score_data in enumerate(scores):
                rank_text = f"{i + 1}."
                name_text = score_data["name"]
                score_text = str(score_data["score"])
                level_text = f"Level {score_data['level']}"

                text = f"{rank_text:4} {name_text:15} {score_text:8} {level_text}"
                score_surf = self.renderer.font_small.render(text, True, color_manager.get_color("COLOR_TEXT"))
                score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                self.screen.blit(score_surf, score_rect)
                y_pos += 35

        # Back instruction
        back_surf = self.renderer.font_small.render("Press ESC to go back", True, color_manager.get_color("COLOR_TEXT"))
        back_rect = back_surf.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.screen.blit(back_surf, back_rect)

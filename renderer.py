"""
Renderer module for displaying the game.
"""

import pygame
from config import (
    COLOR_WALL, COLOR_PATH, COLOR_PLAYER, COLOR_EXIT,
    COLOR_OBSTACLE, COLOR_COLLECTIBLE, COLOR_BACKGROUND,
    COLOR_TEXT, COLOR_MENU_BG, CELL_SIZE, SCREEN_WIDTH,
    SCREEN_HEIGHT, TILE_WALL, TILE_EXIT
)

class Renderer:
    """Handles all game rendering."""
    
    def __init__(self, screen):
        """Initialize renderer."""
        self.screen = screen
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
    
    def render_maze(self, maze, offset_x=0, offset_y=0):
        """Render the maze layout."""
        for y, row in enumerate(maze.layout):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * CELL_SIZE + offset_x,
                    y * CELL_SIZE + offset_y,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                # Draw tile
                if tile == TILE_WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                    pygame.draw.rect(self.screen, (60, 60, 60), rect, 1)
                elif tile == TILE_EXIT:
                    pygame.draw.rect(self.screen, COLOR_EXIT, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_PATH, rect)
        
        # Draw collectibles
        for col_x, col_y in maze.collectibles:
            if (col_x, col_y) not in maze.collected:
                center_x = col_x * CELL_SIZE + CELL_SIZE // 2 + offset_x
                center_y = col_y * CELL_SIZE + CELL_SIZE // 2 + offset_y
                pygame.draw.circle(
                    self.screen,
                    COLOR_COLLECTIBLE,
                    (center_x, center_y),
                    CELL_SIZE // 4
                )
        
        # Draw obstacles
        for obs_x, obs_y in maze.obstacles:
            rect = pygame.Rect(
                obs_x * CELL_SIZE + offset_x,
                obs_y * CELL_SIZE + offset_y,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
    
    def render_player(self, player, offset_x=0, offset_y=0):
        """Render the player."""
        rect = pygame.Rect(
            player.x + offset_x,
            player.y + offset_y,
            CELL_SIZE,
            CELL_SIZE
        )
        margin = CELL_SIZE // 4
        inner_rect = rect.inflate(-margin * 2, -margin * 2)
        pygame.draw.rect(self.screen, COLOR_PLAYER, inner_rect, border_radius=5)
    
    def render_hud(self, level, score, collectibles, time_remaining, lives):
        """Render the heads-up display."""
        y_pos = 10
        
        # Level
        level_text = self.font_small.render(f"Level: {level}", True, COLOR_TEXT)
        self.screen.blit(level_text, (10, y_pos))
        
        # Score
        score_text = self.font_small.render(f"Score: {score}", True, COLOR_TEXT)
        self.screen.blit(score_text, (150, y_pos))
        
        # Collectibles
        col_text = self.font_small.render(f"Items: {collectibles}", True, COLOR_TEXT)
        self.screen.blit(col_text, (300, y_pos))
        
        # Time
        if time_remaining is not None:
            time_text = self.font_small.render(f"Time: {int(time_remaining)}s", True, COLOR_TEXT)
            self.screen.blit(time_text, (450, y_pos))
        
        # Lives
        lives_text = self.font_small.render(f"Lives: {lives}", True, COLOR_TEXT)
        self.screen.blit(lives_text, (600, y_pos))
    
    def render_menu(self, title, options, selected_index):
        """Render a menu screen."""
        self.screen.fill(COLOR_MENU_BG)
        
        # Title
        title_surf = self.font_large.render(title, True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Options
        y_start = 250
        for i, option in enumerate(options):
            color = (255, 255, 100) if i == selected_index else COLOR_TEXT
            option_surf = self.font_medium.render(option, True, color)
            option_rect = option_surf.get_rect(center=(SCREEN_WIDTH // 2, y_start + i * 60))
            self.screen.blit(option_surf, option_rect)
            
            if i == selected_index:
                # Draw selection indicator
                indicator = ">"
                ind_surf = self.font_medium.render(indicator, True, color)
                ind_rect = ind_surf.get_rect(center=(option_rect.left - 30, option_rect.centery))
                self.screen.blit(ind_surf, ind_rect)
    
    def render_message(self, message, submessage=None):
        """Render a centered message."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLOR_MENU_BG)
        self.screen.blit(overlay, (0, 0))
        
        # Main message
        text_surf = self.font_large.render(message, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(text_surf, text_rect)
        
        # Submessage
        if submessage:
            sub_surf = self.font_medium.render(submessage, True, COLOR_TEXT)
            sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(sub_surf, sub_rect)
    
    def render_game_over(self, final_score, level_reached):
        """Render game over screen."""
        self.screen.fill(COLOR_MENU_BG)
        
        # Game Over text
        title_surf = self.font_large.render("GAME OVER", True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        
        # Stats
        score_surf = self.font_medium.render(f"Final Score: {final_score}", True, COLOR_TEXT)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_surf, score_rect)
        
        level_surf = self.font_medium.render(f"Level Reached: {level_reached}", True, COLOR_TEXT)
        level_rect = level_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(level_surf, level_rect)
        
        # Continue instruction
        continue_surf = self.font_small.render("Press ENTER to continue", True, COLOR_TEXT)
        continue_rect = continue_surf.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(continue_surf, continue_rect)
    
    def render_victory(self, final_score):
        """Render victory screen."""
        self.screen.fill(COLOR_MENU_BG)
        
        # Victory text
        title_surf = self.font_large.render("CONGRATULATIONS!", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        
        subtitle_surf = self.font_medium.render("You completed all levels!", True, COLOR_TEXT)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # Final score
        score_surf = self.font_medium.render(f"Final Score: {final_score}", True, COLOR_TEXT)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_surf, score_rect)
        
        # Continue instruction
        continue_surf = self.font_small.render("Press ENTER to continue", True, COLOR_TEXT)
        continue_rect = continue_surf.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(continue_surf, continue_rect)
    
    def get_maze_offset(self, maze):
        """Calculate offset to center maze on screen."""
        maze_width = maze.width * CELL_SIZE
        maze_height = maze.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_height) // 2 + 20  # Account for HUD
        return offset_x, offset_y
    
    def clear(self):
        """Clear the screen."""
        self.screen.fill(COLOR_BACKGROUND)

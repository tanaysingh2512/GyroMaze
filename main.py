"""
Main entry point for the maze game.
"""

import pygame
import sys
from game_manager import GameManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Initialize and run the game."""
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    
    # Create game manager
    game_manager = GameManager(screen)
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Update game state
        if not game_manager.update(events, dt):
            running = False
        
        # Render
        game_manager.render()
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

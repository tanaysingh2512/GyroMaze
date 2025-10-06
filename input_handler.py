"""
Input handler module with abstract base class for easy switching between input methods.
This allows for easy transition from keyboard to gyroscopic sensor input.
"""

from abc import ABC, abstractmethod
import pygame

class InputHandler(ABC):
    """Abstract base class for input handling."""
    
    @abstractmethod
    def get_direction(self):
        """
        Get the current movement direction.
        Returns: tuple (dx, dy) where values are -1, 0, or 1
        """
        pass
    
    @abstractmethod
    def update(self, events):
        """Update input state based on events."""
        pass


class KeyboardInputHandler(InputHandler):
    """Keyboard input handler using arrow keys or WASD."""
    
    def __init__(self):
        self.dx = 0
        self.dy = 0
    
    def get_direction(self):
        """Get movement direction from keyboard input."""
        return (self.dx, self.dy)
    
    def update(self, events):
        """Update direction based on keyboard state."""
        keys = pygame.key.get_pressed()
        
        # Reset direction
        self.dx = 0
        self.dy = 0
        
        # Check arrow keys and WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 1
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = 1


class GyroscopeInputHandler(InputHandler):
    """
    Gyroscope input handler for Raspberry Pi.
    This is a placeholder implementation - you'll need to integrate
    with your specific gyroscope sensor library.
    """
    
    def __init__(self, sensitivity=1.0):
        self.dx = 0
        self.dy = 0
        self.sensitivity = sensitivity
        # TODO: Initialize gyroscope sensor here
        # Example: self.sensor = MPU6050()
    
    def get_direction(self):
        """Get movement direction from gyroscope."""
        return (self.dx, self.dy)
    
    def update(self, events):
        """
        Update direction based on gyroscope readings.
        This is a placeholder - implement based on your sensor.
        """
        # TODO: Read from gyroscope sensor
        # Example:
        # accel_data = self.sensor.get_accel_data()
        # tilt_x = accel_data['x']
        # tilt_y = accel_data['y']
        # 
        # Convert tilt to direction (-1, 0, 1)
        # self.dx = self._normalize_tilt(tilt_x)
        # self.dy = self._normalize_tilt(tilt_y)
        pass
    
    def _normalize_tilt(self, tilt_value):
        """
        Convert tilt value to -1, 0, or 1.
        Adjust threshold based on your sensor sensitivity.
        """
        threshold = 0.2 * self.sensitivity
        if tilt_value < -threshold:
            return -1
        elif tilt_value > threshold:
            return 1
        return 0

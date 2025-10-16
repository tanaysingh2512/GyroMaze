"""
Input handlers for the Maze game.

- KeyboardInputHandler: WASD/Arrow keys for 4-directional movement.
  (Prevents diagonal moves by favoring horizontal input.)

- SenseHatGyroInputHandler: Uses Sense HAT IMU for tilt-to-move.
  Roll -> left/right, Pitch -> up/down, with deadzone + smoothing.
  Quick shake (accelerometer magnitude spike) => "confirm" gesture
  which you can map to Enter by posting a KEYDOWN(K_RETURN) or by
  calling .consume_confirm() from the game loop.

Both handlers expose:
  - update(events)
  - get_direction() -> (dx, dy) where dx,dy in {-1,0,1}
"""

from __future__ import annotations
import math
import time
import pygame


# ----------------------------- Base -----------------------------

class InputHandler:
    def update(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    def get_direction(self) -> tuple[int, int]:
        return (0, 0)


# --------------------------- Keyboard ---------------------------

class KeyboardInputHandler(InputHandler):
    """
    Simple keyboard handler (WASD / Arrow keys).
    Prevents diagonal moves: if both axes are pressed, prefers horizontal.
    """
    def __init__(self) -> None:
        self.dx = 0
        self.dy = 0

    def update(self, events: list[pygame.event.Event]) -> None:
        # (We don't need to read events for continuous movement, but keeping the signature.)
        keys = pygame.key.get_pressed()

        # Horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -1
        else:
            self.dx = 0

        # Vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = 1
        else:
            self.dy = 0

        # Prevent diagonal grid moves (keep 4-directional)
        if self.dx != 0 and self.dy != 0:
            # Favor horizontal when both are pressed
            self.dy = 0

    def get_direction(self) -> tuple[int, int]:
        return (self.dx, self.dy)


# ---------------------------- Sense HAT ----------------------------

class SenseHatGyroInputHandler(InputHandler):
    """
    Tilt control via Sense HAT IMU.
      - Roll  -> dx (left/right)
      - Pitch -> dy (up/down)

    Features:
      - Deadzone (degrees) to ignore tiny hand shakes
      - EMA smoothing for stable tilt values
      - Shake detection (accelerometer magnitude threshold) for a "confirm" gesture

    Use .consume_confirm() once-per-gesture in your game code to act like Enter.
    """

    def __init__(
        self,
        deadzone_deg: float = 8.0,
        smooth: float = 0.25,
        shake_g_threshold: float = 1.7,
        shake_debounce_ms: float = 800.0
    ) -> None:
        try:
            from sense_hat import SenseHat  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "Sense HAT library not found. Install on the Pi with: sudo apt install sense-hat"
            ) from e

        self.sense = SenseHat()
        # Orientation baseline (pitch0, roll0) set on first update or after recalibration
        self._baseline: tuple[float, float] | None = None

        # Configuration
        self.deadzone = float(deadzone_deg)
        self.smooth = float(smooth)
        self.shake_g = float(shake_g_threshold)
        self.shake_debounce = float(shake_debounce_ms) / 1000.0

        # Smoothed pitch/roll (EMA)
        self._fp = 0.0
        self._fr = 0.0

        # Direction output
        self.dx = 0
        self.dy = 0

        # Shake/confirm state
        self._last_confirm_ts = 0.0
        self._confirm_pending = False

    # ------------------------ helpers ------------------------

    @staticmethod
    def _wrap180(a: float) -> float:
        """Wrap angle to [-180, 180] for stable differences."""
        while a > 180:
            a -= 360
        while a < -180:
            a += 360
        return a

    def _read_orientation(self) -> tuple[float, float]:
        """
        Returns (pitch, roll) in degrees from Sense HAT.
        get_orientation() gives keys: 'pitch', 'roll', 'yaw'
        """
        o = self.sense.get_orientation()
        return float(o["pitch"]), float(o["roll"])

    def _read_accel_g(self) -> float:
        """
        Returns accelerometer magnitude in g (gravity = ~1.0g).
        """
        a = self.sense.get_accelerometer_raw()  # dict with x,y,z in g
        return math.sqrt(a["x"] ** 2 + a["y"] ** 2 + a["z"] ** 2)

    # ---------------------- public API -----------------------

    def update(self, events: list[pygame.event.Event]) -> None:
        # Optional: allow manual recalibration via keyboard (SPACE/C) when using VNC
        for e in events:
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_c):
                self._baseline = None

        pitch, roll = self._read_orientation()

        # Initialize baseline if needed
        if self._baseline is None:
            self._baseline = (pitch, roll)

        # Relative angles, then wrap to [-180, 180]
        pitch = self._wrap180(pitch - self._baseline[0])
        roll  = self._wrap180(roll  - self._baseline[1])

        # Exponential moving average smoothing
        self._fp = (1.0 - self.smooth) * self._fp + self.smooth * pitch
        self._fr = (1.0 - self.smooth) * self._fr + self.smooth * roll

        # Map to discrete axis with deadzone
        ax = 0
        ay = 0
        if   self._fr >  self.deadzone: ax =  1
        elif self._fr < -self.deadzone: ax = -1

        if   self._fp >  self.deadzone: ay =  1
        elif self._fp < -self.deadzone: ay = -1

        # Avoid diagonals: prefer stronger tilt axis
        if ax != 0 and ay != 0:
            if abs(self._fr) >= abs(self._fp):
                ay = 0
            else:
                ax = 0

        self.dx, self.dy = ax, ay

        # Gesture detection: quick shake => confirm
        mag_g = self._read_accel_g()
        now = time.time()
        if mag_g >= self.shake_g and (now - self._last_confirm_ts) >= self.shake_debounce:
            self._confirm_pending = True
            self._last_confirm_ts = now

    def get_direction(self) -> tuple[int, int]:
        return (self.dx, self.dy)

    def consume_confirm(self) -> bool:
        """
        Returns True once when a shake gesture is detected.
        Use this in your state handlers (menu/level-complete) to simulate Enter.
        """
        if self._confirm_pending:
            self._confirm_pending = False
            return True
        return False

## SETTINGS

import math

# game settings

# Screen resolution
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
# Frame Rate
FPS = 60

# Initial player settings
PLAYER_POS = 1.5, 5  # mini map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

# Mouse settings
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

# Player field of view
FOV = math.pi / 3   # FOV is 1/3 of a circle
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # Uses half of screen resolution (WIDTH) to define number of rays
# '//' integer division operator. Similar to Math.floor(). Will always round down.
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS    # angle between rays
MAX_DEPTH = 20

# Screen location, view needs to be somewhere between player and full distance for useful FOV.
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

# Texture settings
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

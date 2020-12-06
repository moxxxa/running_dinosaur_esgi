SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
ENEMY_SCALING = 0.8
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.95
PLAYER_JUMP_SPEED = 20
SCROOL_SPEED = 8

REWARD_STUCK = -2000
REWARD_DOWN = -10
REWARD_UP = -10
REWARD_DEFAULT = 0


UP, DOWN, WALK = 'U', 'D', 'W'
ACTIONS = [WALK, DOWN, UP]

DEFAULT_LEARNING_RATE = 1
DEFAULT_DISCOUNT_FACTOR = 0.5

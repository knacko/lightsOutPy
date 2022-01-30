
adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

# This is the distance multiplier to enable gaps between the polygons
DISTANCE = 1.1

# This is the scale multiplier. All coordinates for polygons are done with a unit length of 1,
# so this is the number of pixels per unit length
SCALE = 50
BORDER = 25

# Set the state colors
ON_COLOR = (255, 0, 0)
OFF_COLOR = (0, 255, 0)
SOLVE_COLOR = (0, 0, 0)

GRID_SIZE = [6, 6]

GAME_SIZE = (GRID_SIZE[0] * SCALE, GRID_SIZE[1]*SCALE)
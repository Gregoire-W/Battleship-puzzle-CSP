# Regular import
import numpy as np

# Core Objects
from csp import CSP
from game import Game

# Utils
from utils.config_loader import ConfigLoader as cl
from utils.utils import get_surrounding_cells

# Constraints
from constraints.m_constraint import MConstraint
from constraints.border_constraint import BorderConstraint
from constraints.check import Check as ck

config_file = cl.get_config("Input/init.txt")
rows, cols = config_file["board"].shape

# Variables, we consider every case of the board
config_file["variables"] = [(x, y) for x in range(rows) for y in range(cols)]
game = Game(**config_file)


# Domains
max_variable = game.max_boat_size()
rows, cols = game.get_shape
domains = {}

for x, y in game.variables: 
    domains[(x, y)] = [i for i in range(max_variable+1)]
    # If there is a M at this pos, the cell can't take the value 0, 1 and 2 beause it's the middle of a boat
    if game.board[x, y] != "0":  # To avoid testing each sign every time because most of the time valur will be 0
        if game.board[x, y] == "M":
            for i in range(3):
                domains[(x, y)].remove(i)
        # If there is any of this sign ["<", ">", "^", "v"] at this pos, the cell can't take the value 0 and 1 because it's a boat extermity
        elif game.board[x, y] in ["<", ">", "^", "v"]:
            for i in range(2):
                domains[(x, y)].remove(i)


# Constraints
constraints = {variable : [] for variable in game.variables}
for variable in game.variables:
    x, y = variable
    # Add border constraints
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            # Skip the center cell itself (x, y)
            if (i, j) == (x, y):
                continue
            # Check if the coordinate is within bounds
            if 0 <= i < rows and 0 <= j < cols:
                constraints[variable].append(BorderConstraint((i, j)))
    if game.board[x, y] == "M":
        cells = get_surrounding_cells((x, y), rows, cols)
        for current_cell in cells:
            constraints[current_cell].append(MConstraint([cell for cell in cells if cell != current_cell]))
        

global_constraints = [
    ck.respect_cardinality,
    ck.check_boat_size,
    ck.check_nb_boat,
]


# Solve the BattleShip puzzle using CSP
csp = CSP(game, domains, constraints, global_constraints)
csp.max_degree

sol = csp.solve()

# Format the solution for output
# Step 1: Determine grid dimensions
max_row = max(key[0] for key in sol.keys()) + 1
max_col = max(key[1] for key in sol.keys()) + 1

# Step 2: Create an empty NumPy array
grid = np.zeros((max_row, max_col), dtype=int)

# Step 3: Fill the array with values from the dictionary
print('*'*7, 'Solution', '*'*7)
for (row, col), value in sol.items():
    grid[row, col] = value
print(grid)
csp.display_performance()
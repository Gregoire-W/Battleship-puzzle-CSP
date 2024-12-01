from csp import CSP
from config_loader import ConfigLoader as cl
from check import Check as ck
from game import Game
import numpy as np
from border_constraint import BorderConstraint
from utils import get_surrounding_cells
from m_constraint import MConstraint

config_file = cl.get_config("init.txt")
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
    if game.board[x, y] == "M":
        for i in range(3):
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
print('*'*7, 'Solution', '*'*7)
csp = CSP(game, domains, constraints, global_constraints)
sol = csp.solve()

# Format the solution for output
# Step 1: Determine grid dimensions
max_row = max(key[0] for key in sol.keys()) + 1
max_col = max(key[1] for key in sol.keys()) + 1

# Step 2: Create an empty NumPy array
grid = np.zeros((max_row, max_col), dtype=int)

# Step 3: Fill the array with values from the dictionary
for (row, col), value in sol.items():
    grid[row, col] = value
print(grid)
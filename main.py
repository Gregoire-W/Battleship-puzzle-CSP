from csp import CSP
from config_loader import ConfigLoader as cl
from constraints import Constraints as cst
from boat import Boat
from game import Game

config_file = cl.get_config("init.txt")

# Variables
variables = []
for size, number in enumerate(config_file["variables"]):
    variables += [Boat(size+1) for i in range(number)]

config_file["variables"] = variables

game = Game(**config_file)
# print(cst.respect_cardinality(None, {0: [(0, 0)], 1: [(0, 2)], 2: [(0, 4)], 3: [(2, 1), (3, 1)], 4: [(3, 3), (4, 3)], 5: [(2, 5), (3, 5), (4, 5)]}, game))
# input()

# Domains
rows, cols = game.get_shape
domains = {}
for var in variables:
    domains[var.id] = []
    for row in range(rows):
        for col in range(cols):
            domains[var.id].append([(row+x, col) for x in range(var.size)])
            if var.size > 1:
                domains[var.id].append([(row, col+x) for x in range(var.size)])

# Constraints
constraints = [
    cst.inside_map,
    cst.is_border_zero,
    cst.not_stacked,
    cst.respect_cardinality,
]

# Initial constraints
initial_constraints = [
    cst.respect_hints
]

# Solve the BattleShip puzzle using CSP
print('*'*7, 'Solution', '*'*7)
csp = CSP(game, domains, constraints, initial_constraints)
sol = csp.solve()

# Format the solution for output
print(sol)
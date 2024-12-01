# Regular import
import numpy as np

def main(
    config_path,
    loader,
    m_constraint_builder,
    border_constraint_builder,
    game_builder,
    csp_builder,
    global_constraints,
    get_surrounding_cells,
    get_adjacent_cell,
    output_path,
):


    config_file = loader.get_config(config_path)
    rows, cols = config_file["board"].shape

    # Variables, we consider every case of the board
    config_file["variables"] = [(x, y) for x in range(rows) for y in range(cols)]
    game = game_builder(**config_file)


    # Domains
    max_variable = game.max_boat_size
    rows, cols = game.get_shape
    domains = {(x, y): [i for i in range(max_variable+1)] for x, y in game.variables}


    for x, y in game.variables: 
        # If there is a M at this pos, the cell can't take the value 0, 1 and 2 beause it's the middle of a boat
        if game.board[x, y] != "0":  # To avoid testing each sign every time because most of the time valur will be 0
            if game.board[x, y] == "M":
                for i in range(3):
                    domains[(x, y)].remove(i)
            # If there is any of this sign ["<", ">", "^", "v"] at this pos, the cell can't take the value 0 and 1 because it's a boat extermity
            elif game.board[x, y] in ["<", ">", "^", "v"]:
                # Also remove values from the adjacent cell depending on sign orientation
                cell = get_adjacent_cell((x, y), game.board[x, y], rows, cols)
                if(cell):
                    for i in range(2):
                        domains[(x, y)].remove(i)
                        domains[cell].remove(i)
                else:
                    raise ValueError("There is no possible solution for this input file")
            elif game.board[x, y] == "S":
                domains[(x, y)] = [1]
                cells = get_surrounding_cells((x, y), rows, cols)
                for cell in cells:
                    domains[cell] = [0]



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
                    constraints[variable].append(border_constraint_builder((i, j)))
        if game.board[x, y] != "0":
            if game.board[x, y] == "M":
                cells = get_surrounding_cells((x, y), rows, cols)
                for current_cell in cells:
                    constraints[current_cell].append(m_constraint_builder([cell for cell in cells if cell != current_cell]))


    glb_constraints = [
        global_constraints.respect_cardinality,
        global_constraints.check_boat_size,
        global_constraints.check_nb_boat,
    ]


    # Solve the BattleShip puzzle using CSP
    csp = csp_builder(game, domains, constraints, glb_constraints, get_surrounding_cells)

    # Chose heuristics, ordering or filter that can make algorithm faster
    # Heuristic : mrv, max_degree
    # Ordering : lcv
    # Filter : forward_check, ac3
    # Example bellow
    csp.lcv
    csp.forward_check
    csp.mrv
    #csp.forward_check
    #csp.ac3

    csp.solve()
    csp.save_solution(output_path)

    csp.display_solution()
    csp.display_performance()
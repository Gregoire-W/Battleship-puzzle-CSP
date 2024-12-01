class Check:

    @staticmethod
    def check_border_value(value, var, constraints_cells, assignement, game):
        if value > 0:
            diagonals = [border for border in constraints_cells if abs(border[0] - var[0]) == 1 and abs(border[1] - var[1]) == 1]
            other = [cell for cell in constraints_cells if cell not in diagonals]
            for cell in diagonals:
                if cell in assignement and assignement[cell] != 0:
                    return False
            liste = [0] if value == 1 else [0, value]
            for cell in other:
                if cell in assignement and assignement[cell] not in liste:
                    return False
        return True


    @staticmethod
    def respect_cardinality(value, var, constraints_cells, assignement, game):
        rows, cols = game.get_shape
        row, col = var
        boat_counts = [1, 1] if value > 0 else [0, 0] # We count the current boat in initialization
        water_counts = [1, 1] if value == 0 else [0, 0] # We count the current boat in initialization
        for x, y in assignement.keys():
            if x == row:
                if assignement[x, y] > 0:
                    boat_counts[0] += 1
                else:
                    water_counts[0] += 1
            if y == col:
                if assignement[x, y] > 0:
                    boat_counts[1] += 1
                else:
                    water_counts[1] += 1
        boat_cond = boat_counts[0] <= game.rows[row] and boat_counts[1] <= game.cols[col]  # Not more boats than accepeted 
        water_cond = water_counts[0] <= rows - game.rows[row] and water_counts[1] <= cols - game.cols[col]
        return boat_cond and water_cond

    @staticmethod
    def check_boat_size(value, var, constraints_cells, assignement, game):
        if value > 0:
            count = [0, 0, 0, 0]
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # [Right, Left, Down, Up]
            for k, direction in enumerate(directions):
                for i in range(1, value+1):
                    x, y = var[0] + i* direction[0], var[1] + i* direction[1]
                    if (x, y) in assignement and assignement[(x, y)] == value:
                        count[k] += 1
                    else:
                        break
            max_shape = max(count[0] + count[1], count[2] + count[3])  # Max between horizontal and vertical biggest shape
            if value < 1 + max_shape:
                return False
        return True
    
    @staticmethod
    def check_nb_boat(value, var, constraints_cells, assignement, game):
        if value > 0:
            count = list(assignement.values()).count(value)
            return (count + 1) / value <= game.boats[value]  # +1 to count the boat we are trying to place
        return True

# print(Check.check_boat_size(2, (0, 5), None, {(0, 0): 0, (0, 1): 0, (0, 2): 2, (0, 3): 2, (0, 4): 2, (1, 0): 0, (1, 1): 0, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 1, (3, 0): 0, (3, 1): 2, (3, 2): 2, (3, 3): 2, (3, 4): 0, (3, 5): 0, (4, 0): 0, (4, 1): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 1, (5, 0): 0, (5, 1): 0, (5, 2): 0, (5, 3): 1, (5, 4): 0, (5, 5): 0}, None))



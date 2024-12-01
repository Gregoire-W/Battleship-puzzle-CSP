class GlobalConstraints:
    """This class is a storage class that contains the definition of all global constraints"""

    @staticmethod
    def respect_cardinality(value, var, assignement, game):
        """
        Checks that the cardinality constraint is always respected
        - value: The value of the cell in parameter
        - var: The cell that is getting a new value
        - assignement: The current assignement of CSP
        - game: the loaded game informations

        Returns True if condition is respected, else False.
        """
        rows, cols = game.get_shape
        row, col = var
        boat_counts = [1, 1] if value > 0 else [0, 0] # We check the current value in initialization
        water_counts = [1, 1] if value == 0 else [0, 0] # We check the current value in initialization
        # Count every boats and water cells for each rows and columns
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
        # boat_counts can't be superior than game.rows in each row and game.cols in each col
        boat_cond = boat_counts[0] <= game.rows[row] and boat_counts[1] <= game.cols[col]
        # we also need to check if there is still enough space for the require number of boat
        water_cond = water_counts[0] <= rows - game.rows[row] and water_counts[1] <= cols - game.cols[col]
        return boat_cond and water_cond

    @staticmethod
    def check_boat_size(value, var, assignement, game):
        """
        Checks that the boat size constraint is always respected
        - value: The value of the cell in parameter
        - var: The cell that is getting a new value
        - assignement: The current assignement of CSP
        - game: the loaded game informations

        Returns True if condition is respected, else False.
        """
        if value > 0:
            count = [0, 0, 0, 0]
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # [Right, Left, Down, Up]
            for k, direction in enumerate(directions):
                for i in range(1, value+1):
                    x, y = var[0] + i* direction[0], var[1] + i* direction[1]
                    # Every time we see the same boat we add 1
                    if (x, y) in assignement and assignement[(x, y)] == value:
                        count[k] += 1
                    # As soon as we see something else we stop because we check continuity
                    else:
                        break
            # We check that the boat is not part of a larger series of cells than its value.
            max_shape = max(count[0] + count[1], count[2] + count[3])  # Max between horizontal and vertical biggest shape
            if value < 1 + max_shape:
                return False
        return True

    @staticmethod
    def check_nb_boat(value, var, assignement, game):
        """
        Checks that the number of boats constraint is always respected
        - value: The value of the cell in parameter
        - var: The cell that is getting a new value
        - assignement: The current assignement of CSP
        - game: the loaded game informations

        Returns True if condition is respected, else False.
        """
        if value > 0:
            count = list(assignement.values()).count(value)
            return (count + 1) / value <= game.boats[value]  # +1 to count the boat we are trying to place
        return True
class Constraints:

    @staticmethod
    def inside_map(boat_pos, assignement, game):
        rows, cols = game.get_shape
        return all([(x >= 0 and x < rows and y >= 0 and y < cols) for x, y in boat_pos])
    
    @staticmethod
    def is_border_zero(boat_pos, assignement, game):
        occupied_cells = set(cell for cells in assignement.values() for cell in cells)
        rows = [coord[0] for coord in boat_pos]
        cols = [coord[1] for coord in boat_pos]

        # Determine the bounding box
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        # Generate border cells
        border_cells = set()
        for row in range(min_row - 1, max_row + 2):
            for col in range(min_col - 1, max_col + 2):
                if (row, col) not in boat_pos:  # Exclude boat cells
                    border_cells.add((row, col))

        return all(cell not in occupied_cells for cell in border_cells)

    
    @staticmethod
    def not_stacked(boat_pos, assignement, game):
        return all([(x, y) not in pos for (x, y) in boat_pos for pos in assignement.values()])

    @staticmethod
    def respect_cardinality(boat_pos, assignement, game):
        rows, cols = game.get_shape
        row_counts, col_counts = {row: 0 for row in range(rows)}, {col: 0 for col in range(cols)}
        for position in assignement.values():
            for row, col in position :
                row_counts[row] += 1
                col_counts[col] += 1
        for row, col in boat_pos:
            row_counts[row] += 1
            col_counts[col] += 1
        all_rows = all([row_counts[row] <= game.rows[row] for row in range(rows)])
        all_cols = all([col_counts[col] <= game.cols[col] for col in range(cols)])
        return all_rows and all_cols
    
    @staticmethod
    def respect_hints(boat_pos, assignement, game):
        rows, cols = game.get_shape
        all_positions = set(cell for cells in assignement.values() for cell in cells)
        m_positions = [(row, col) for row in range(rows) for col in range(cols) if game.board[row, col] == "M"]

        for row, col in m_positions:
            # Check if the 'M' position is in the dictionary
            if (row, col) not in all_positions:
                return False
            else:
                # Define adjacent pairs
                horizontal_pair = [(row, col - 1), (row, col + 1)]  # Left and right
                vertical_pair = [(row - 1, col), (row + 1, col)]    # Top and bottom

                # Check if both positions in either pair are in the valid positions
                horizontal_valid = all(pos in all_positions for pos in horizontal_pair)
                vertical_valid = all(pos in all_positions for pos in vertical_pair)
                
                # If neither condition is satisfied, return False
                if not (horizontal_valid or vertical_valid):
                    return False
            
            # If all checks passed
            return True

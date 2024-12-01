def get_surrounding_cells(cell, rows, cols):
    """
    Finds all the cells stuck directly to the one passed as a parameter (not the diagonal cells)
    - cell: The cell whose neighbours we are looking for
    - rows: Rows number of the board
    - cols: Cols number of the board

    Returns all the cells stuck to the one in parameter and which are present in the range of our board.
    """
    x, y = cell
    surrounding_cells = []
    # Top:
    if x - 1 >= 0:
        surrounding_cells.append((x - 1, y))
    # Bottom:
    if x + 1 < rows:
        surrounding_cells.append((x + 1, y))
    # Left:
    if y - 1 >= 0:
        surrounding_cells.append((x, y - 1))
    # Right:
    if y + 1 < cols:
        surrounding_cells.append((x, y + 1))
    return surrounding_cells


def get_adjacent_cell(cell, sign, rows, cols):
    """
    Finds the cell adjacent to the one passed in parameter based on its sign in the input file
    - cell: The cell whose adjacent cell we are looking for
    - sign: The sign of the cell in the input file
    - rows: Rows number of the board
    - cols: Cols number of the board

    Returns the adjacent cell to the one in parameter and None if its doesn't exist
    """
    x, y = cell

    if sign == ">":
        new_coord = (x, y - 1)  # Right
    elif sign == "<":
        new_coord = (x, y + 1)  # Left
    elif sign == "v":
        new_coord = (x - 1, y)  # Down
    elif sign == "^":
        new_coord = (x + 1, y)  # Up
    else:
        raise ValueError("Invalid sign. Must be one of '>', '<', 'v', '^'.")

    # Check if the new coordinate is within the map range
    new_x, new_y = new_coord
    if 0 <= new_x < rows and 0 <= new_y < cols:
        return new_coord
    else:
        return None
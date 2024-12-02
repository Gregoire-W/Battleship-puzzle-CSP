import numpy as np

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
    
def format_solution(solution):
    """
    This method format the dictonnary solution to a numpy array so it can be easier to use it (for instance to save or display it). 
    Each cell is represented by a specific character indicating its status (empty, ship, or part of a boat).
    - output_path: The file path where the solution will be saved.

    Solution Representation:
    - "." indicates an empty cell.
    - "S" indicates a standalone ship (size 1).
    - "M" indicates the middle part of a boat (size > 1).
    - "<", ">", "v", "^" indicate directional parts of a boat:

    Raises:
    - ValueError: If a boat cell is surrounded by more than two other boat cells.
    """
    max_row = max(key[0] for key in solution.keys()) + 1
    max_col = max(key[1] for key in solution.keys()) + 1
    array_solution = np.full((max_row, max_col), ".", dtype = str)  # Put . by default for water so we don"t have to check it

    for (row, col), value in solution.items():
        if value == 1:
            array_solution[row][col] = "S"
        elif value > 1:
            cells = get_surrounding_cells((row, col), max_row, max_col)
            nb_surrounding_boat = sum([1 for value in cells if solution[value] > 0])
            if nb_surrounding_boat == 2:
                array_solution[row][col] = "M"
            elif nb_surrounding_boat == 1:
                cell = [cell for cell in cells if solution[cell] > 0][0]
                if cell == (row, col+1):  # cell is at right
                    array_solution[row][col] = "<"
                elif cell == (row, col-1):  # cell is at left
                    array_solution[row][col] = ">"
                elif cell == (row - 1, col):  # cell is up
                    array_solution[row][col] = "v"
                else:  # cell is down
                    array_solution[row][col] = "^"
            else :
                raise ValueError("Boat is supposed to be surrounded only by 1 or 2 boats")
    return array_solution
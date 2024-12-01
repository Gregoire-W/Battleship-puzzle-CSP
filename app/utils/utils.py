def get_surrounding_cells(cell, rows, cols):
    x, y = cell
    surrounding_cells = []

    # Check the 4 surrounding positions: top, bottom, left, right
    # Top: (x-1, y)
    if x - 1 >= 0:
        surrounding_cells.append((x - 1, y))
    
    # Bottom: (x+1, y)
    if x + 1 < rows:
        surrounding_cells.append((x + 1, y))
    
    # Left: (x, y-1)
    if y - 1 >= 0:
        surrounding_cells.append((x, y - 1))
    
    # Right: (x, y+1)
    if y + 1 < cols:
        surrounding_cells.append((x, y + 1))
    
    return surrounding_cells


def get_adjacent_cell(cell, sign, rows, cols):
    x, y = cell

    # Compute the new coordinate based on the direction sign
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
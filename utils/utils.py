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
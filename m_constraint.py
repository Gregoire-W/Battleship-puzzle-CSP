class MConstraint:

    def __init__(self, surrounding_cells):
        self.surrounding_cells = surrounding_cells

    def is_valid(self, value, var, assignement, game):

        if all(cell in assignement for cell in self.surrounding_cells):

            horizontal_surrounding = []
            vertical_surrounding = []
            
            x, y = var 
            
            # For each pair of surrounding cells
            for i, (sx, sy) in enumerate(self.surrounding_cells):
                for (tx, ty) in self.surrounding_cells[i+1:]:
                    if sx == tx:  # Same row -> horizontal
                        horizontal_surrounding.extend([(sx, sy), (tx, ty)])
                        break
                    elif sy == ty:  # Same column -> vertical
                        vertical_surrounding.extend([(sx, sy), (tx, ty)])
                        break
                
            not_found, found = (horizontal_surrounding, vertical_surrounding)  if horizontal_surrounding == [] else (vertical_surrounding, horizontal_surrounding)

            not_found.extend([cell for cell in self.surrounding_cells if cell not in found])
            not_found.append(var)

            return all(assignement[cell] != 0 for cell in found) or all(assignement[cell] != 0 for cell in not_found)
        return True
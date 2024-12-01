from constraints.constraint import Constraint

class MConstraint(Constraint):

    def __init__(self, surrounding_cells):
        self.surrounding_cells = surrounding_cells

    def is_valid(self, value, var, assignement, game):

        if all(cell in assignement for cell in self.surrounding_cells):

            horizontal_surrounding = []
            vertical_surrounding = []
            
            # For each pair of surrounding cells
            for i, (sx, sy) in enumerate(self.surrounding_cells):
                for (tx, ty) in self.surrounding_cells[i+1:]:
                    if sx == tx:  # Same row -> horizontal
                        horizontal_surrounding.extend([(sx, sy), (tx, ty)])
                        break
                    elif sy == ty:  # Same column -> vertical
                        vertical_surrounding.extend([(sx, sy), (tx, ty)])
                        break
            
            # As soon as we found one, we know the other so let's determine which one we found
            found = vertical_surrounding if horizontal_surrounding == [] else horizontal_surrounding
            last_cell = [cell for cell in self.surrounding_cells if cell not in found][0]

            return all(assignement[cell] != 0 for cell in found) or (assignement[last_cell] != 0 and value != 0)
        return True
    
    @property
    def involved_cells(self):
        return self.surrounding_cells
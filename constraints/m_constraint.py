from constraints.constraint import Constraint

class MConstraint(Constraint):
    """This class ensures that the cells involved in the M constraint respect it"""

    def __init__(self, surrounding_cells):
        self.surrounding_cells = surrounding_cells


    def is_valid(self, value, var, assignement, game):
        """
        Checks that the constraint is still respected when one of the 4 variables takes a new value
        - value: The value of the cell in parameter
        - var: The cell that is getting a new value
        - assignement: The current assignement of CSP
        - game: the loaded game informations

        Returns True if condition is respected, else False.
        """
        #Check only if every the 4 variables around the M have a value
        if all(cell in assignement for cell in self.surrounding_cells):
            # We need to identify which are the horizontal and vertical cells
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

            # Check if both horizontal cells or both vertical cells are a boat
            return all(assignement[cell] != 0 for cell in found) or (assignement[last_cell] != 0 and value != 0)
        return True


    @property
    def involved_cells(self):
        """
        Returns every cells involved in this constraint except the one that created it.
        """
        return self.surrounding_cells
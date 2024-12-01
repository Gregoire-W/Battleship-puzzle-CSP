from constraints.constraint import Constraint

class BorderConstraint(Constraint):
    """This class ensures that the cells involved in the board constraint respect it"""
    def __init__(self, border_cell):
        self.border_cell = border_cell

    def is_valid(self, value, var, assignement, game):
        """
        Checks that the constraint is still respected when the variable get a value
        - value: The value of the cell in parameter
        - var: The cell that is getting a new value
        - assignement: The current assignement of CSP
        - game: the loaded game informations

        Returns True if condition is respected, else False.
        """
        # Check if cell involved in this constraint is a diagonal of the one that created it
        diagonal = True if abs(self.border_cell[0] - var[0]) == 1 and abs(self.border_cell[1] - var[1]) == 1 else False
        # Verify only if the value is a boat, water can be surrounded by anything
        if value > 0:
            liste = [0] if value == 1 else [0, value]
            # If it is a diagonal it must be 0
            if diagonal and self.border_cell in assignement:
                return assignement[self.border_cell] == 0
            # If not it must be the same boat or water (excpeted submarine that accept only water)
            elif not diagonal and self.border_cell in assignement:
                return assignement[self.border_cell] in liste
        return True

    @property
    def involved_cells(self):
        """
        Returns the border cell involved in this constraint.
        """
        return [self.border_cell]
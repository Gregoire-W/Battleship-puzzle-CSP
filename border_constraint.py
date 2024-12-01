class BorderConstraint():

    def __init__(self, border_cell):
        self.border_cell = border_cell
    
    def is_valid(self, value, var, assignement, game):
        diagonal = True if abs(self.border_cell[0] - var[0]) == 1 and abs(self.border_cell[1] - var[1]) == 1 else False
        if value > 0:
            liste = [0] if value == 1 else [0, value]
            if diagonal and self.border_cell in assignement:
                return assignement[self.border_cell] == 0
            elif not diagonal and self.border_cell in assignement:
                return assignement[self.border_cell] in liste
        return True
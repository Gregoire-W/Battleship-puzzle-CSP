class Game:
    """This class is used to centralise all the information for the game loaded"""

    def __init__(self, rows, cols, board, variables, boats):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.variables = variables
        self.boats = {k+1: v for k, v in enumerate(boats)}
        self.boats = {k: v for k, v in self.boats.items() if v != 0}


    @property
    def get_shape(self):
        """
        Returns the shape of game's board
        """
        return self.board.shape


    def __repr__(self):
        """
        Allows the game and its attributes to be clearly displayed in a list or in a printout

        Returns game informations in a clear string format
        """
        return f"""Game :\nrows : {self.rows}\ncols : {self.cols}\nboard :\n{self.board}\n
        boats : {self.boats}\nvariables : {self.variables}"""


    @property
    def max_boat_size(self):
        """
        Returns maximum size of this game boats
        """
        return max(self.boats.keys())
    
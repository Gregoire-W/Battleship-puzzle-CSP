class Game:

    def __init__(self, rows, cols, board, variables, boats):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.variables = variables
        self.boats = {k+1: v for k, v in enumerate(boats)}
        self.boats = {k: v for k, v in self.boats.items() if v != 0}

    @property
    def get_shape(self):
        return self.board.shape
    


    def __repr__(self):
        return f"""Game :\nrows : {self.rows}\ncols : {self.cols}\nboard :\n{self.board}\n
        boats : {self.boats}\nvariables : {self.variables}"""
    

    @property
    def max_boat_size(self):
        return max(self.boats.keys())
        
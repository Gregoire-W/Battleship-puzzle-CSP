class Game:

    def __init__(self, rows, cols, board, variables):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.variables = variables

    @property
    def get_shape(self):
        return self.board.shape
    
    def __repr__(self):
        return f"Game :\nrows : {self.rows}\ncols : {self.cols}\nboard :\n{self.board}\nboats : {self.variables}"
        
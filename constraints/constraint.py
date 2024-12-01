class Constraint:

    
    def is_valid(self):
        raise NotImplementedError(f"method is_valid should be implemented in class : {type(self).__name__}")
    
    @property
    def involved_cells(self):
        raise NotImplementedError(f"property involved_cells should be implemented in class : {type(self).__name__}")
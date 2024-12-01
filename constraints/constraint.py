class Constraint:
    """This class ensures that the cells involved in the M constraint respect it."""

    def is_valid(self):
        """
        Raises an error when the method is called from this class
        """
        raise NotImplementedError(f"method is_valid should be implemented in class : {type(self).__name__}")


    @property
    def involved_cells(self):
        """
        Raises an error when the property is called from this class
        """
        raise NotImplementedError(f"property involved_cells should be implemented in class : {type(self).__name__}")
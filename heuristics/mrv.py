from heuristics.heuristic import Heuristic

class MRV(Heuristic):

    @staticmethod
    def get_type():
        return "variable"

    @staticmethod
    def apply(unassigned_variable, csp):
        """
        This method implements the Minimum Remaining Values (MRV) heuristic, which selects the variable with the fewest possible values
        remaining in its domain. This heuristic helps prioritize variables that are most constrained, reducing the search space
        - unassigned_vars: A list of variables that have not yet been assigned a value
        - assignment: the current variable assignment of the CSP

        Returns:
        - A list of variables from "unassigned_vars" that have the smallest domain size (minimum remaining values)
        If there is a tie, all variables with the smallest domain size are returned for potential future heuristics
        """
        min_value = min(len(csp.domains[var]) for var in unassigned_variable)
        values = [var for var in unassigned_variable if len(csp.domains[var]) == min_value]
        return values
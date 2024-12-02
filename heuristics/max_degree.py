from heuristics.heuristic import Heuristic

class MaxDegree(Heuristic):

    @staticmethod
    def get_type(self):
        return "variable"

    @staticmethod
    def apply(unassigned_variable, csp):
        """
        This method implements the Degree heuristic, which selects the variable involved in the most constraints with other
        unassigned variables. This heuristic helps prioritize variables that are most likely to influence the search space
        - unassigned_vars: A list of variables that have not yet been assigned a value
        - assignment: the current variable assignment of the CSP

        Returns:
        - A list of variables from "unassigned_vars" with the highest degree (number of constraints involving other unassigned variables)
            If there is a tie, all variables with the same highest degree are returned for potential future heuristics
        """
        max_degree = -1
        best_variables = []
        for var in unassigned_variable:
            involved_cells = set([cells for constraint in csp.constraints[var] for cells in constraint.involved_cells])
            degree = sum([1 for cell in involved_cells if cell in unassigned_variable])
            if degree > max_degree:
                max_degree = degree
                best_variables = [var]
            elif degree >= max_degree:
                best_variables.append(var)
        return best_variables
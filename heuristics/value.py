from heuristics.heuristic import Heuristic

h_type = "value"

class LCV(Heuristic):

    @staticmethod
    def get_type():
        return h_type

    @staticmethod
    def apply(var, csp):
        """
        This property implements the Least Constraining Value (LCV) heuristic, which orders the domain values of a variable based on
        how minimally they constrain the remaining variables. Values that leave the most options open for other variables are preferred
        - var: The variable for which the domain values are being ordered
        - assignment: the current variable assignment of the CSP

        Returns:
        - A list of domain values for the variable "var", ordered by their impact on the remaining unassigned variables.
            Values that constrain the least are placed first
        """
        values = []
        for value in csp.domains[var]:
            csp.assignment[var] = value
            involved_cells = set([cells for constraint in csp.constraints[var] for cells in constraint.involved_cells])
            possible_value = 0
            for cell in involved_cells:
                if cell not in csp.assignment:
                    for cell_value in csp.domains[cell]:
                        if csp.is_consistent(cell, cell_value):
                            possible_value += 1
            values.append((value, possible_value))
            del csp.assignment[var]
        ordered_values = sorted(values, key=lambda x: x[1], reverse=True)
        return [x[0] for x in ordered_values]
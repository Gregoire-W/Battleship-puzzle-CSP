from heuristics.heuristic import Heuristic

h_type = "fw_ck"

class ForwardCheck(Heuristic):
    
    @staticmethod
    def get_type():
        return h_type

    @staticmethod
    def apply(csp, var):
            """
            This method implements forward checking, a constraint propagation technique used during backtracking search
            It prunes the domains of unassigned variables to ensure consistency with the current assignment, reducing the search space
            - var: the variable that has just been assigned a value.

            Returns
            - True if forward checking doesn't fail, else False.
            - a dictionnary of removed value to keep it in memory
            """
            involved_cells = set([cells for constraint in csp.constraints[var] for cells in constraint.involved_cells])
            removed_values = {}
            for cell in involved_cells:
                if cell not in csp.assignment:
                    fixed_values = csp.domains[cell].copy()  # Otherwise the loop misses values because it deletes them
                    for cell_value in fixed_values:
                        if not csp.is_consistent(cell, cell_value):
                            csp.domains[cell].remove(cell_value)
                            if cell in removed_values:
                                removed_values[cell].append(cell_value)
                            else:
                                removed_values[cell] = [cell_value]
                            csp.pruned_values += 1
                if not csp.domains[cell]:
                    return False, removed_values
            return True, removed_values
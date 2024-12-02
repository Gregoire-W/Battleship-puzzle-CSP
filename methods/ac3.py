from methods.method import Method

m_type = "ac3"

class AC3(Method):

    @staticmethod
    def get_type():
        return m_type

    @staticmethod
    def apply(csp):
        """
        This is the AC-3 (Arc Consistency 3) method, used to reduce the domains of variables by enforcing arc consistency before applying backtracking.
        It ensures that every variable in the CSP has a valid domain with respect to its constraints, thereby simplifying the problem.
        - assignment: the current variable assignment of the CSP

        Returns True if all variables still have available values, else False
        """
        queue = [(cell, cst_cell) for cell in csp.game.variables for cst_cell in set([cells for constraint in csp.constraints[cell] for cells in constraint.involved_cells])]
        while queue:
            (cell, cst_cell) = queue.pop()
            if AC3.remove_inconsistent_values(cell, cst_cell, csp):
                if not csp.domains[cell]:  # If cell has no value left, return False
                    return False
                for _cell in set([cells for constraint in csp.constraints[cell] for cells in constraint.involved_cells]):
                    if _cell != cst_cell:
                        queue.append((_cell, cst_cell))
        return True
    

    @staticmethod
    def remove_inconsistent_values(cell, cst_cell, csp):
        """
        This function removes inconsistent values from the domain of a variable to ensure arc consistency
        It checks whether there is a value in the domain of one variable that conflicts with all possible values of its neighbor,
        removing such inconsistent values
        - cell: the cell we want to ensure arc consistency
        - cst_cell: the neighboring cell involved in the constraint with cell
        - assignment: the current variable assignment of the CSP

        Returns True if at least a variable lost a value, else False
        """
        removed = False
        for value in csp.domains[cell]:
            csp.assignment[cell] = value
            if not any(csp.is_consistent(cst_cell, cst_value) for cst_value in csp.domains[cst_cell]):
                csp.domains[cell].remove(value)
                removed = True
            del csp.assignment[cell]
        return removed
class CSP:
    def __init__(self, game, Domains, constraints, initial_constraints):
        self.game = game
        self.domains = Domains
        self.constraints = constraints
        self.initial_constraints = initial_constraints
        self.solution = None

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.game.variables):
            return assignment

        var_id = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var_id, assignment):
            if self.is_consistent(var_id, value, assignment):
                assignment[var_id] = value
                result = self.backtrack(assignment)
                if result is not None and all(initial_constraint(None, assignment, self.game) for initial_constraint in self.initial_constraints):
                    return result
                del assignment[var_id]
        return None
    
    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var.id for var in self.game.variables if var.id not in assignment]
        return min(unassigned_vars, key=lambda var_id: len(self.domains[var_id]))

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints:
            if not constraint(value, assignment, self.game):
                return False
        return True
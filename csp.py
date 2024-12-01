class CSP:

    variable_checked = 0

    def __init__(self, game, Domains, constraints, global_constraints, heuristic = lambda x: x[0]):
        self.game = game
        self.domains = Domains
        self.constraints = constraints
        self.heuristic = heuristic  # By default if no heuristic we return the first element
        self.global_constraints = global_constraints
        self.solution = None


    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution


    def backtrack(self, assignment):
        if len(assignment) == len(self.game.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        CSP.variable_checked += 1
        for value in self.order_domain_values(var, assignment):
            # input(["INPUT"])
            # print(f"try value {value} in pos {var}")
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None
    

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.game.variables if var not in assignment]
        return self.heuristic(unassigned_vars)


    def order_domain_values(self, var, assignment):
        return self.domains[var]


    def is_consistent(self, var, value, assignment):
        constraints = self.constraints[var]
        global_csts = all(check(value, var, constraints, assignment, self.game) for check in self.global_constraints)
        individual_csts = all(constraint.is_valid(value, var, assignment, self.game) for constraint in constraints)
        # print([check(value, var, constraints, assignment, self.game) for check in self.consistence_checks])
        return global_csts and individual_csts
    

    @property
    def mrv(self):
        self.heuristic = lambda unassigned_vars: min(unassigned_vars, key=lambda var: len(self.domains[var]))


    @property
    def lcv(self):
        self.heuristic = lambda unassigned_vars : min(unassigned_vars, key=lambda var: len(self.constraints[var]))
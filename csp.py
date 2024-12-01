import time

class CSP:

    def __init__(self, game, domains, constraints, global_constraints, heuristics = []):
        self.game = game
        self.domains = domains
        self.constraints = constraints
        self.heuristics = heuristics  # By default if no heuristics we return the first element
        self.global_constraints = global_constraints
        self.solution = None

        # Some performance metrics
        self.node_expansions = 0
        self.number_of_backtracks = 0
        self.pruned_values = 0
        self.number_of_constraint_checks = 0
        # time calculation
        self.start_time = None
        self.end_time = None


    def solve(self):
        assignment = {}
        self.start_time = time.time()  # Start the timer
        self.solution = self.backtrack(assignment)
        self.end_time = time.time()
        return self.solution


    def backtrack(self, assignment):
        if len(assignment) == len(self.game.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                self.node_expansions += 1
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
                self.number_of_backtracks += 1
        return None
    

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.game.variables if var not in assignment]
        if self.heuristics == []:
            return unassigned_vars[0]
        for heuristic in self.heuristics:
            unassigned_vars = heuristic(unassigned_vars, assignment)
        return unassigned_vars[0]


    def order_domain_values(self, var, assignment):
        return self.domains[var]


    def is_consistent(self, var, value, assignment):
        constraints = self.constraints[var]
        for cst in constraints:
            self.number_of_constraint_checks += 1
            res = cst.is_valid(value, var, assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        for glb_cst in self.global_constraints:
            self.number_of_constraint_checks += 1
            res = glb_cst(value, var, constraints, assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        return True
    

    @property
    def mrv(self):
        def lambda_mrv(unassigned_vars, assignment):
            min_value = min(len(self.domains[var]) for var in unassigned_vars)
            values = [var for var in unassigned_vars if len(self.domains[var]) == min_value]
            return values
        self.heuristics.append(lambda_mrv)


    @property
    def lcv(self):
        def lambda_lcv(unassigned_vars, assignment):
            min_value = min(len(self.constraints[var]) for var in unassigned_vars)
            values = [var for var in unassigned_vars if len(self.constraints[var]) == min_value]
            return values
        self.heuristics.append(lambda_lcv)

    @property
    def max_degree(self):
        def lambda_degree(unassigned_vars, assignment):
            max_degree = -1
            best_variables = []
            for var in unassigned_vars:
                involved_cells = set([cells for constraint in self.constraints[var] for cells in constraint.involved_cells])
                degree = sum([1 for cell in involved_cells if cell not in assignment])
                if degree > max_degree:
                    max_degree = degree
                    best_variables = [var]
                elif degree >= max_degree:
                    best_variables.append(var)
            return best_variables
        self.heuristics.append(lambda_degree)

    def display_performance(self):
        """Display the performance of the CSP solver."""
        print("Time taken: {:.4f} seconds".format(self.end_time - self.start_time))
        print("Node expansions: {}".format(self.node_expansions))
        print("Number of Backtracks: {}".format(self.number_of_backtracks))
        print("Number of Constraint Checks: {}".format(self.number_of_constraint_checks))
        print("Pruned values: {}".format(self.pruned_values))

    @property
    def reset_heuristic(self):
        self.heuristic = []
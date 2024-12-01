import time
import numpy as np

class CSP:

    def __init__(self, game, domains, constraints, global_constraints, get_surrounding_cells, heuristics = [], order = None, strategy = None, use_ac3 = False):
        self.game = game
        self.domains = domains
        self.constraints = constraints
        self.heuristics = heuristics  # By default if no heuristics we return the first element
        self.order = order
        self.strategy = strategy
        self.global_constraints = global_constraints
        self.get_surrounding_cells = get_surrounding_cells
        self.use_ac3 = use_ac3
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
        if self.use_ac3:
            self._ac3(assignment)
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
                if self.strategy:
                    cond, removed_values = self.strategy(var, value, assignment)
                else:
                    cond, removed_values = True, {}
                if cond:
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                # Get back every removed values
                for k, values in removed_values.items():
                    if k in self.domains:
                        self.domains[k].extend([val for val in values])
                    else:
                        self.domains[k] = [val for val in values]

                del assignment[var]
                self.number_of_backtracks += 1
        return None
    
    @property
    def ac3(self):
        self.use_ac3 = True


    @property
    def remove_ac3(self):
        self.use_ac3 = False


    def _ac3(self, assignment):
        queue = [(cell, cst_cell) for cell in self.game.variables for cst_cell in set([cells for constraint in self.constraints[cell] for cells in constraint.involved_cells])]
        while queue:
            (cell, cst_cell) = queue.pop()
            if self.remove_inconsistent_values(cell, cst_cell, assignment):
                if not self.domains[cell]:  # If cell has no value left, return False
                    return False
                for _cell in set([cells for constraint in self.constraints[cell] for cells in constraint.involved_cells]):
                    if _cell != cst_cell:
                        queue.append((_cell, cst_cell))
        return True

    def remove_inconsistent_values(self, cell, cst_cell, assignment):
        removed = False
        for value in self.domains[cell]:
            assignment[cell] = value
            if not any(self.is_consistent(cst_cell, cst_value, assignment) for cst_value in self.domains[cst_cell]):
                self.domains[cell].remove(value)
                removed = True
            del assignment[cell]
        return removed

    @property
    def forward_check(self):
        def lambda_forward_check(var, value, assignment):
            involved_cells = set([cells for constraint in self.constraints[var] for cells in constraint.involved_cells])
            removed_values = {}
            for cell in involved_cells:
                if cell not in assignment:
                    fixed_values = self.domains[cell].copy()  # Otherwise the loop misses values because it deletes them
                    for cell_value in fixed_values:
                        if not self.is_consistent(cell, cell_value, assignment):
                            self.domains[cell].remove(cell_value)
                            if cell in removed_values:
                                removed_values[cell].append(cell_value)
                            else:
                                removed_values[cell] = [cell_value]
                            self.pruned_values += 1
                if not self.domains[cell]:
                    return False, removed_values
            return True, removed_values
        self.strategy = lambda_forward_check
    

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.game.variables if var not in assignment]
        if self.heuristics == []:
            return unassigned_vars[0]
        for heuristic in self.heuristics:
            unassigned_vars = heuristic(unassigned_vars, assignment)
        return unassigned_vars[0]


    def order_domain_values(self, var, assignment):
        if not self.order:
            return self.domains[var]
        else:
            return self.order(var, assignment)


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
        def lambda_lcv(var, assignment):
            values = []
            for value in self.domains[var]:
                assignment[var] = value
                involved_cells = set([cells for constraint in self.constraints[var] for cells in constraint.involved_cells])
                possible_value = 0
                for cell in involved_cells:
                    if cell not in assignment:
                        for cell_value in self.domains[cell]:
                            if self.is_consistent(cell, cell_value, assignment):
                                possible_value += 1
                values.append((value, possible_value))
                del assignment[var]
            ordered_values = sorted(values, key=lambda x: x[1], reverse=True)
            return [x[0] for x in ordered_values]
        self.order = lambda_lcv


    @property
    def reset_order(self):
        self.order = None


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


    def display_solution(self):
        # Format the solution for output
        # Step 1: Determine grid dimensions
        max_row = max(key[0] for key in self.solution.keys()) + 1
        max_col = max(key[1] for key in self.solution.keys()) + 1

        # Step 2: Create an empty NumPy array
        grid = np.zeros((max_row, max_col), dtype=int)

        # Step 3: Fill the array with values from the dictionary
        print('*'*7, 'Solution', '*'*7)
        for (row, col), value in self.solution.items():
            grid[row, col] = value
        print(grid)


    @property
    def reset_heuristic(self):
        self.heuristic = []

    def save_solution(self, output_path):
        max_row = max(key[0] for key in self.solution.keys()) + 1
        max_col = max(key[1] for key in self.solution.keys()) + 1

        with open(output_path, "w") as f:
            sorted_solution = dict(sorted(self.solution.items(), key=lambda item: (item[0][0], item[0][1])))
            for (row, col), value in sorted_solution.items():
                if(row != 0 and col == 0):
                    f.write("\n")
                if value == 0:
                    write = "."
                elif value == 1:
                    write = "S"
                else:  # value > 1
                    cells = self.get_surrounding_cells((row, col), max_row, max_col)
                    nb_surrounding_boat = sum([1 for value in cells if sorted_solution[value] > 0])
                    if nb_surrounding_boat == 2:
                        write = "M"
                    elif nb_surrounding_boat == 1:
                        cell = [cell for cell in cells if sorted_solution[cell] > 0][0]
                        if cell == (row, col+1):  # cell is at right
                            write = "<"
                        elif cell == (row, col-1):  # cell is at left
                            write = ">"
                        elif cell == (row - 1, col):  # cell is up
                            write = "v"
                        else:  # cell at is down
                            write = "^"
                    else:
                        raise ValueError("Boat is supposed to be surrounded only by 1 or 2 boats")
                f.write(write)

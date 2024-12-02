import time
import numpy as np
import copy

class CSP:
    """This class models a CSP and can be used to solve a problem as long as it has been properly defined.
    It also has several different heuristics that can be compared and the option of saving the solution found.
    """

    def __init__(self, game, domains, constraints, global_constraints, format_solution):
        self.game = game
        self.domains = domains
        self.initial_domain = copy.deepcopy(domains)
        self.constraints = constraints
        self.strategy = None
        self.global_constraints = global_constraints
        self.format_solution = format_solution
        self.use_ac3 = False
        self.solution = None
        self.heuristics = {h: [] for h in ["variable", "value"]}
        self.assignment = {} 

        # Some performance metrics
        self.node_expansions = 0
        self.number_of_backtracks = 0
        self.pruned_values = 0
        self.number_of_constraint_checks = 0

        # time calculation
        self.start_time = None
        self.end_time = None


    def solve(self):
        """
        This is the csp solver method that will search for the solution with the specified heuristics.

        Returns the result if it exists, else None .
        """
        self.start_time = time.time()
        if self.use_ac3:
            self._ac3()
        self.solution = self.backtrack()
        self.end_time = time.time()
        return self.solution


    def backtrack(self):
        """
        This is the backtracking method, which will allow us to examine all the possibilities of the search tree that respect the constraints.
        It stops when the final solution has been found or when all the possibilities have been explored.
        - assignment : the current variable assignment of the CSP

        Returns the result if it exists, else None .
        """
        if len(self.assignment) == len(self.game.variables):
            return self.assignment

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.node_expansions += 1
                self.assignment[var] = value
                if self.strategy:
                    cond, removed_values = self.strategy(var)
                else:
                    cond, removed_values = True, {}
                if cond:
                    result = self.backtrack()
                    if result is not None:
                        return result

                # Get back every removed values
                for k, values in removed_values.items():
                    if k in self.domains:
                        self.domains[k].extend([val for val in values])
                    else:
                        self.domains[k] = [val for val in values]

                del self.assignment[var]
                self.number_of_backtracks += 1
        return None


    def select_unassigned_variable(self):
        """
        Selects a variable that has not yet been assigned. If one or more heuristics have been specified, this method uses them for its selection
        - assignment: the current variable assignment of the CSP

        Returns the unassigned variable selectionned
        """
        unassigned_vars = [var for var in self.game.variables if var not in self.assignment]
        for heuristic in self.heuristics["variable"]:
            unassigned_vars = heuristic.apply(unassigned_vars, self)
        return unassigned_vars[0]


    def order_domain_values(self, var):
        """
        Orders the possible values of a variable with a heuristic if it has been specified, otherwise keeps the basic order
        - var : the variable that we want to order values
        - assignment: the current variable assignment of the CSP

        Returns the variable values ordered with specified heuristic
        """
        variables = self.domains[var]
        for heuristic in self.heuristics["value"]: 
            variables = heuristic.apply(var, self)
        return variables


    def is_consistent(self, var, value):
        """
        This method checks that all constraints are met when a value is given to a variable
        - var: the variable that we want to test a value
        - value: the value tested for the variable.
        - assignment: the current variable assignment of the CSP

        Returns True if the variable with this value respect all constraint, else False
        """
        constraints = self.constraints[var]
        for cst in constraints: # Unit constraints
            self.number_of_constraint_checks += 1
            res = cst.is_valid(value, var, self.assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        for glb_cst in self.global_constraints: #Global constraints
            self.number_of_constraint_checks += 1
            res = glb_cst(value, var, self.assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        return True


    @property
    def ac3(self):
        """
        Adds the AC3 algorithm to reduce variable domains if this method is called before .solve()
        """
        self.use_ac3 = True


    @property
    def remove_ac3(self):
        """
        Remove the AC3 algorithm if this method is called before .solve()
        """
        self.use_ac3 = False


    def _ac3(self):
        """
        This is the AC-3 (Arc Consistency 3) method, used to reduce the domains of variables by enforcing arc consistency before applying backtracking.
        It ensures that every variable in the CSP has a valid domain with respect to its constraints, thereby simplifying the problem.
        - assignment: the current variable assignment of the CSP

        Returns True if all variables still have available values, else False
        """
        queue = [(cell, cst_cell) for cell in self.game.variables for cst_cell in set([cells for constraint in self.constraints[cell] for cells in constraint.involved_cells])]
        while queue:
            (cell, cst_cell) = queue.pop()
            if self.remove_inconsistent_values(cell, cst_cell):
                if not self.domains[cell]:  # If cell has no value left, return False
                    return False
                for _cell in set([cells for constraint in self.constraints[cell] for cells in constraint.involved_cells]):
                    if _cell != cst_cell:
                        queue.append((_cell, cst_cell))
        return True

    def remove_inconsistent_values(self, cell, cst_cell):
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
        for value in self.domains[cell]:
            self.assignment[cell] = value
            if not any(self.is_consistent(cst_cell, cst_value, self.assignment) for cst_value in self.domains[cst_cell]):
                self.domains[cell].remove(value)
                removed = True
            del self.assignment[cell]
        return removed

    @property
    def forward_check(self):
        def lambda_forward_check(var):
            """
            This method implements forward checking, a constraint propagation technique used during backtracking search
            It prunes the domains of unassigned variables to ensure consistency with the current assignment, reducing the search space
            - var: the variable that has just been assigned a value.

            Returns
            - True if forward checking doesn't fail, else False.
            - a dictionnary of removed value to keep it in memory
            """
            involved_cells = set([cells for constraint in self.constraints[var] for cells in constraint.involved_cells])
            removed_values = {}
            for cell in involved_cells:
                if cell not in self.assignment:
                    fixed_values = self.domains[cell].copy()  # Otherwise the loop misses values because it deletes them
                    for cell_value in fixed_values:
                        if not self.is_consistent(cell, cell_value):
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


    def display_performance(self):
        """
        Display the performance metrics of the CSP solver after execution.

        This method provides insights into the solver's efficiency and effectiveness by showing key statistics such as time taken,
        node expansions, backtracking occurrences, constraint checks, and the number of pruned values.

        Performance Metrics:
        - Time taken: The total duration (in seconds) for the CSP solver to complete.
        - Node expansions: The number of nodes in the search tree that were expanded during the solving process.
        - Number of backtracks: The total number of times the solver reverted decisions due to constraint violations.
        - Number of constraint checks: The total number of constraint evaluations performed during the solving process.
        - Pruned values: The total number of values removed from variable domains during constraint propagation.
        """
        print("Time taken: {:.4f} seconds".format(self.end_time - self.start_time))
        print("Node expansions: {}".format(self.node_expansions))
        print("Number of Backtracks: {}".format(self.number_of_backtracks))
        print("Number of Constraint Checks: {}".format(self.number_of_constraint_checks))
        print("Pruned values: {}".format(self.pruned_values))


    def display_solution(self):
        """
        Display the solution of the CSP in a formatted grid.
        """
        grid_solution = self.format_solution(self.solution)
        rows, cols = grid_solution.shape
        for row in range(rows):
            for col in range(cols):
                end = "\n" if col == cols-1 and row != rows else ""
                print(grid_solution[row][col] + " ", end = end)


    def save_solution(self, output_path):
        """
        This method writes the solution to a specified file path.
        - output_path: path where the file will be saved
        """
        grid_solution = self.format_solution(self.solution)
        rows, cols = grid_solution.shape
        with open(output_path, "w") as f:
            for row in range(rows):
                for col in range(cols):
                    if(row != 0 and col == 0):
                        f.write("\n")
                    f.write(grid_solution[row][col])


    @property
    def reset_metrics(self):
        """
        This property resets the key performance metrics used to track the solver's progress.
        It is useful for starting fresh when running with another heuristic for example.
        """
        self.node_expansions = 0
        self.number_of_backtracks = 0
        self.pruned_values = 0
        self.number_of_constraint_checks = 0

    @property
    def reset_all(self):
        """
        This property reset all things below for the initial values
        - heuristics
        - order
        - forward checking
        - ac3
        - domains
        - metrics
        - assignement
        """
        self.heuristics = []
        self.order = None
        self.strategy = None
        self.remove_ac3
        self.reset_metrics
        self.domains = copy.deepcopy(self.initial_domain)
        self.assignment = {}

    def add_heuristics(self, heuristics):
        for h in heuristics:
            if h.get_type() in self.heuristics:
                self.heuristics[h.get_type()].append(h)
            else:
                raise ValueError(f"Type {h.get_type()} : is not accepted [in heuristic : {type(h).__name__}]")
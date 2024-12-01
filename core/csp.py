import time
import numpy as np
import copy

class CSP:
    """This class models a CSP and can be used to solve a problem as long as it has been properly defined.
    It also has several different heuristics that can be compared and the option of saving the solution found.
    """

    def __init__(self, game, domains, constraints, global_constraints, get_surrounding_cells, heuristics = [], order = None, strategy = None, use_ac3 = False):
        self.game = game
        self.domains = domains
        self.initial_domain = copy.deepcopy(domains)
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
        """
        This is the csp solver method that will search for the solution with the specified heuristics.

        Returns the result if it exists, else None .
        """
        assignment = {}
        self.start_time = time.time()
        if self.use_ac3:
            self._ac3(assignment)
        self.solution = self.backtrack(assignment)
        self.end_time = time.time()
        return self.solution


    def backtrack(self, assignment):
        """
        This is the backtracking method, which will allow us to examine all the possibilities of the search tree that respect the constraints.
        It stops when the final solution has been found or when all the possibilities have been explored.
        - assignement : the current variable assignement of the CSP

        Returns the result if it exists, else None .
        """
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


    def _ac3(self, assignment):
        """
        This is the AC-3 (Arc Consistency 3) method, used to reduce the domains of variables by enforcing arc consistency before applying backtracking.
        It ensures that every variable in the CSP has a valid domain with respect to its constraints, thereby simplifying the problem.
        - assignment: the current variable assignement of the CSP

        Returns True if all variables still have available values, else False
        """
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
        """
        This function removes inconsistent values from the domain of a variable to ensure arc consistency
        It checks whether there is a value in the domain of one variable that conflicts with all possible values of its neighbor,
        removing such inconsistent values
        - cell: the cell we want to ensure arc consistency
        - cst_cell: the neighboring cell involved in the constraint with cell
        - assignment: the current variable assignement of the CSP

        Returns True if at least a variable lost a value, else False
        """
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
            """
            This method implements forward checking, a constraint propagation technique used during backtracking search
            It prunes the domains of unassigned variables to ensure consistency with the current assignment, reducing the search space
            - var: the variable that has just been assigned a value.
            - value: the value assigned to the variable.
            - assignment: the current variable assignement of the CSP

            Returns
            - True if forward checking doesn't fail, else False.
            - a dictionnary of removed value to keep it in memory
            """
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
        """
        Selects a variable that has not yet been assigned. If one or more heuristics have been specified, this method uses them for its selection
        - assignment: the current variable assignement of the CSP

        Returns the unassigned variable selectionned
        """
        unassigned_vars = [var for var in self.game.variables if var not in assignment]
        if self.heuristics == []:
            return unassigned_vars[0]
        for heuristic in self.heuristics:
            unassigned_vars = heuristic(unassigned_vars, assignment)
        return unassigned_vars[0]


    def order_domain_values(self, var, assignment):
        """
        Orders the possible values of a variable with a heuristic if it has been specified, otherwise keeps the basic order
        - var : the variable that we want to order values
        - assignment: the current variable assignement of the CSP

        Returns the variable values ordered with specified heuristic
        """
        if not self.order:
            return self.domains[var]
        else:
            return self.order(var, assignment)


    def is_consistent(self, var, value, assignment):
        """
        This method checks that all constraints are met when a value is given to a variable
        - var: the variable that we want to test a value
        - value: the value tested for the variable.
        - assignment: the current variable assignement of the CSP

        Returns True if the variable with this value respect all constraint, else False
        """
        constraints = self.constraints[var]
        # Unit constraints
        for cst in constraints:
            self.number_of_constraint_checks += 1
            res = cst.is_valid(value, var, assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        #Global constraints
        for glb_cst in self.global_constraints:
            self.number_of_constraint_checks += 1
            res = glb_cst(value, var, assignment, self.game)
            if not res:
                self.pruned_values += 1  # Increment pruned values if inconsistency is found
                return False
        return True


    @property
    def mrv(self):
        def lambda_mrv(unassigned_vars, assignment):
            """
            This property implements the Minimum Remaining Values (MRV) heuristic, which selects the variable with the fewest possible values
            remaining in its domain. This heuristic helps prioritize variables that are most constrained, reducing the search space
            - unassigned_vars: A list of variables that have not yet been assigned a value
            - assignment: the current variable assignement of the CSP

            Returns:
            - A list of variables from "unassigned_vars" that have the smallest domain size (minimum remaining values)
            If there is a tie, all variables with the smallest domain size are returned for potential future heuristics
            """
            min_value = min(len(self.domains[var]) for var in unassigned_vars)
            values = [var for var in unassigned_vars if len(self.domains[var]) == min_value]
            return values
        self.heuristics.append(lambda_mrv)


    @property
    def lcv(self):
        def lambda_lcv(var, assignment):
            """
            This property implements the Least Constraining Value (LCV) heuristic, which orders the domain values of a variable based on
            how minimally they constrain the remaining variables. Values that leave the most options open for other variables are preferred
            - var: The variable for which the domain values are being ordered
            - assignment: the current variable assignement of the CSP

            Returns:
            - A list of domain values for the variable "var", ordered by their impact on the remaining unassigned variables.
              Values that constrain the least are placed first
            """
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
        """Reset all order chose for the default one"""
        self.order = None


    @property
    def max_degree(self):
        def lambda_degree(unassigned_vars, assignment):
            """
            This property implements the Degree heuristic, which selects the variable involved in the most constraints with other
            unassigned variables. This heuristic helps prioritize variables that are most likely to influence the search space
            - unassigned_vars: A list of variables that have not yet been assigned a value
            - assignment: the current variable assignement of the CSP

            Returns:
            - A list of variables from "unassigned_vars" with the highest degree (number of constraints involving other unassigned variables)
              If there is a tie, all variables with the same highest degree are returned for potential future heuristics
            """
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
        This method organizes the solution stored as a dictionary into a grid representation for easy visualization.
        """
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
    def reset_heuristics(self):
        """Reset all heuristics chose for the default one"""
        self.heuristics = []


    def save_solution(self, output_path):
        """
        This method writes the solution grid to a specified file path. Each cell is represented by a specific character
        indicating its status (empty, ship, or part of a boat). The solution is sorted by row and column for proper formatting.
        - output_path: The file path where the solution will be saved.

        Solution Representation:
        - "." indicates an empty cell.
        - "S" indicates a standalone ship (size 1).
        - "M" indicates the middle part of a boat (size > 1).
        - "<", ">", "v", "^" indicate directional parts of a boat:

        Raises:
        - ValueError: If a boat cell is surrounded by more than two other boat cells.
        """
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

    @property
    def reset_metrics(self):
        """
        This property resets the key performance metrics used to track the solver’s progress.
        It is useful for starting fresh when running with another heuristic for example.
        """
        self.node_expansions = 0
        self.number_of_backtracks = 0
        self.pruned_values = 0
        self.number_of_constraint_checks = 0

    @property
    def reset_all(self):
        """
        This property reset all things below
        - heuristics
        - order
        - forward checking
        - ac3
        - domains
        - metrics
        """
        self.reset_heuristics
        self.reset_order
        self.strategy = None
        self.remove_ac3
        self.reset_metrics
        self.domains = copy.deepcopy(self.initial_domain)
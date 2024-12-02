# Core Objects
from core.csp import CSP
from core.game import Game

# Constraints
from constraints.m_constraint import MConstraint
from constraints.border_constraint import BorderConstraint
from constraints.global_constraints import GlobalConstraints

# Heuristics
from heuristics.value import LCV
from heuristics.variable import MRV, MaxDegree
from heuristics.ac3 import AC3
from heuristics.forward_check import ForwardCheck

# Process
from app.process import main

if __name__ == "__main__":
    main(
            config_path = "./input/init.txt",
            output_path = "./output/solution.txt",
            m_constraint_builder = MConstraint,
            border_constraint_builder = BorderConstraint,
            game_builder = Game,
            csp_builder = CSP,
            global_constraints = GlobalConstraints,
            MRV = MRV,
            LCV = LCV,
            MaxDegree = MaxDegree,
            AC3 = AC3,
            ForwardCheck = ForwardCheck,
    )
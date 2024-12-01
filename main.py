# Core Objects
from core.csp import CSP
from core.game import Game

# Utils
from app.utils.config_loader import ConfigLoader
from app.utils.utils import get_surrounding_cells, get_adjacent_cell

# Constraints
from constraints.m_constraint import MConstraint
from constraints.border_constraint import BorderConstraint
from constraints.check import Check

# Process
from app.process import main

if __name__ == "__main__":
    main(
            config_path = "./input/init.txt",
            loader = ConfigLoader,
            m_constraint_builder = MConstraint,
            border_constraint_builder = BorderConstraint,
            game_builder = Game,
            csp_builder = CSP,
            check = Check,
            get_surrounding_cells = get_surrounding_cells,
            get_adjacent_cell = get_adjacent_cell,
    )
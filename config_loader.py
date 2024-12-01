import os
import numpy as np


class ConfigLoader:

    @staticmethod
    def get_config(config_path):
        try:
            if not os.path.exists(config_path):
                raise Exception("File note found")
            if not config_path.endswith(".txt"):
                raise Exception("Input file must have .txt format")

            else:
                with open(config_path, "r") as f:
                    lines = f.read().splitlines()

                    _dict = {}
                    for i, key in enumerate(["rows", "cols", "boats"]):
                        _dict[key] = np.array([int(elem) for elem in lines[i]])
                    _dict["board"] = np.array(
                        [[elem for elem in line] for line in lines[i + 1 :]]
                    )
                    return _dict

        except Exception as e:
            raise Exception(f"In ConfigLoader {e}")
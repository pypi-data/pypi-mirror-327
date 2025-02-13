import h5py
import ast
import operator
from typing import Any, Dict, Tuple

from ossobuco.geometries import *
from ossobuco import Simulation

class Reader:
    def __init__(self, h5_file: str):
        if not h5_file.endswith(".h5"):
            h5_file += ".h5"

        self.h5_file = h5_file

    def get_simulations(self, conditions: dict = {}):
        """
        Retrieve simulations from the HDF5 file that match the given conditions.

        :param conditions: A dictionary containing the conditions to filter simulations.
        :return: A list of Simulation objects that match the conditions.
        """
        matching_simulations = []

        with h5py.File(self.h5_file, "r") as f:
            for sim_hash in f.keys():
                group = f[sim_hash]
                
                # Check if the simulation matches the provided conditions
                if self.match_conditions(group, conditions):
                    # If the simulation matches, reconstruct the gap object and store it
                    gap_class_name = group["gap_class"][()].decode("utf-8")
                    gap_class = globals().get(gap_class_name)

                    if gap_class is None:
                        raise ValueError(f"Class {gap_class_name} not found. Please ensure it is imported.")

                    # Reconstruct parameters and geometry
                    parameters = ast.literal_eval(group["parameters"][()].decode("utf-8"))
                    geometry_params = ast.literal_eval(group["geometry_parameters"][()].decode("utf-8"))
                    
                    # Create the gap object with the parameters
                    gap_object = gap_class(parameters, **geometry_params)
                    
                    # Retrieve results (similarly to how it is done in `read_simulation`)
                    gap_object.npart = group["npart"][()]
                    gap_object.gapinteraction = group["gapinteraction"][()]
                    gap_object.set_h_up(group["h_up"][()])
                    gap_object.set_h_low(group["h_low"][()])
                    gap_object.average_h = group["average_h"][()]

                    gap_object.gap_volume = group["gap_volume"][()]
                    gap_object.particles_volume = group["particles_volume"][()]
                    gap_object.vpart_over_vgap = group["vpart_over_vgap"][()]
                    gap_object.k_tracker = group["k_tracker"][()]
                    gap_object.filling_displayer_low = group["filling_displayer_low"][()]
                    gap_object.filling_displayer_up = group["filling_displayer_up"][()]

                    # Create the Simulation object with the reconstructed gap object
                    simulation = Simulation(gap=gap_object, h5_file=self.h5_file)

                    # Add the Simulation object to the results list
                    matching_simulations.append(simulation)

        return matching_simulations

    def match_conditions(self, group, conditions):
        """
        Helper method to check if a simulation matches the given conditions.
        
        :param group: The HDF5 group for a simulation.
        :param conditions: A dictionary with conditions to match.
        :return: True if the simulation matches the conditions, False otherwise.
        """
        for key, value in conditions.items():
            if key == "gap_class":
                # Check if the gap_class matches
                if group["gap_class"][()].decode("utf-8") != value:
                    return False
            
            elif key == "parameters":
                # Check if the parameters match (they may be nested, so we check sub-values)
                stored_params = ast.literal_eval(group["parameters"][()].decode("utf-8"))
                if not self.match_dict_conditions(stored_params, value):
                    return False

            elif key == "geometry_parameters":
                # Check if the geometry_parameters match
                stored_geom_params = ast.literal_eval(group["geometry_parameters"][()].decode("utf-8"))
                if not self.match_dict_conditions(stored_geom_params, value):
                    return False

        return True

    def match_dict_conditions(self, stored_dict, conditions_dict):
        """
        Helper method to check if the stored dictionary matches the conditions dictionary.
        Supports exact matches and inequality comparisons for numerical values.

        :param stored_dict: The dictionary from the simulation to compare.
        :param conditions_dict: The conditions to match against.
        :return: True if the dictionaries match, False otherwise.
        """
        for key, condition in conditions_dict.items():
            if key not in stored_dict:
                return False
            
            # Determine if the condition specifies an operator and value
            if isinstance(condition, tuple):
                op, value = condition
                if not self.apply_operator(stored_dict[key], op, value):
                    return False
            else:
                # If it's not a tuple, just do an exact match
                if stored_dict[key] != condition:
                    return False

        return True

    def apply_operator(self, value1: Any, operator_str: str, value2: Any) -> bool:
        """
        Apply the comparison operator between two values.

        :param value1: The first value (from stored dictionary).
        :param operator_str: The operator to apply (e.g., ">", "<", "==").
        :param value2: The second value (from conditions).
        :return: True if the comparison holds, False otherwise.
        """
        operators = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne
        }
        
        # Get the corresponding operator function and apply it
        if operator_str not in operators:
            raise ValueError(f"Unsupported operator: {operator_str}")
        
        return operators[operator_str](value1, value2)

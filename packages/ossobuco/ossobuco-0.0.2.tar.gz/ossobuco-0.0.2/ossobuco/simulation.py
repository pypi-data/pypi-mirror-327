# from abc import ABC, abstractmethod
import os
import hashlib
import h5py
import ast

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from ossobuco import Gap
from ossobuco.geometries import *
from ossobuco.utils import myplot


class Simulation:
    def __init__(
        self,
        gap: Gap,
        h5_file: str = None,
        OVERWRITE: bool = False,
    ):

        self.gap = gap
        self.h5_file = h5_file
        self.OVERWRITE = OVERWRITE
        self.param_hash = self.generate_param_hash()

        # fix potential issues regarding h5 file
        if self.h5_file is None:
            self.h5_file = 'default.h5'
            print(f"HDF5 filename is not specified (None). Saving to {self.h5_file}")

        if not self.h5_file.endswith(".h5"):
            self.h5_file += ".h5"

        directory = os.path.dirname(self.h5_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def generate_param_hash(self):
        """
        Generate a unique hash based on both the parameters and the geometry type.
        """
        # Combine the geometry class name and the parameters into a single string
        geometry_type = self.gap.__class__.__name__  # 'Keil', 'Sphere', etc.
        param_str = str(self.gap.parameters)  # Convert parameters to string

        # Create a combined string and hash it
        combined_str = geometry_type + param_str
        return hashlib.sha256(combined_str.encode("utf-8")).hexdigest()

    def check_simulation_exists(self):
        """Checks if the simulation already exists in the HDF5 file."""
        with h5py.File(self.h5_file, "a") as f:
            return self.param_hash in f

    def handle_simulation_overwrite(self, f):
        """
        Checks if the simulation exists and handles overwriting if necessary.
        Returns True if the simulation should be overwritten or newly created, False otherwise.
        """
        if self.check_simulation_exists():
            if not self.OVERWRITE:
                print(f"Simulation exists. Loading existing simulation (to overwrite, set OVERWRITE=True).")
                return False  # Don't overwrite, so we skip the operation.
            else:
                print(f"Overwriting the existing simulation data.")
                del f[
                    self.param_hash
                ]  # Delete the old simulation data before writing new data
                return True  # Proceed with overwriting
        else:
            return True  # Proceed with creating a new simulation (not overwriting)

    def run(self, show_output=True):
        """
        Runs the simulation, fills the gap, computes the gap and particle volumes, and optionally
        displays the results and writes them to an HDF5 file. If the simulation already exists, it
        checks the OVERWRITE flag and either skips or overwrites the simulation accordingly.
        """
        # Open the HDF5 file for appending
        with h5py.File(self.h5_file, "a") as f:
            # Handle overwrite logic and decide whether to run or skip the simulation
            if not self.handle_simulation_overwrite(f):
                self.read_simulation_from_h5()  # Load existing simulation data
                if show_output:
                    self.gap.show_output()  # Display the results
                return  # Skip running the simulation if not overwriting

            # Proceed with running the simulation if we are not skipping
            print("Running new simulation...")
            self.gap.fill()

            # Write the new results to the HDF5 file
            self.write_results_to_h5(f)  # Pass the file handle to avoid reopening it

            # Optionally display the output
            if show_output:
                self.gap.show_output()

    def write_results_to_h5(self, f):
        """
        Writes the simulation results and the gap object to an HDF5 file.
        """
        # Use the passed file object `f` and handle the overwrite logic
        if not self.handle_simulation_overwrite(f):
            return  # If we skip overwriting, simply return

        # Check if the group already exists and delete it if needed
        if self.param_hash in f:
            del f[self.param_hash]

        # Create a new group for the simulation
        group = f.create_group(self.param_hash)

        # store some info as attribute for easier hfive terminal overview
        group.attrs["param_hash"] = self.param_hash
        group.attrs["gap_class"] = self.gap.__class__.__name__

        # Store the class name (this helps us recreate the Gap subclass when reading)
        group.create_dataset(
            "gap_class", data=self.gap.__class__.__name__.encode("utf-8")
        )

        # Store the common parameters
        group.create_dataset(
            "parameters", data=str(self.gap.parameters).encode("utf-8")
        )

        # Store geometry-specific parameters using to_dict method
        geometry_params = self.gap.to_dict()

        group.create_dataset(
            "geometry_parameters", data=str(geometry_params).encode("utf-8")
        )

        # Store the results
        group.create_dataset("npart", data=self.gap.npart)
        group.create_dataset("gapinteraction", data=self.gap.gapinteraction)
        group.create_dataset("h_up", data=self.gap.h_up)
        group.create_dataset("h_low", data=self.gap.h_low)
        group.create_dataset("average_h", data=self.gap.average_h)

        group.create_dataset("gap_volume", data=self.gap.gap_volume)
        group.create_dataset("particles_volume", data=self.gap.particles_volume)
        group.create_dataset("vpart_over_vgap", data=self.gap.vpart_over_vgap)
        group.create_dataset("k_tracker", data=self.gap.k_tracker)
        group.create_dataset(
            "filling_displayer_low", data=self.gap.filling_displayer_low
        )
        group.create_dataset("filling_displayer_up", data=self.gap.filling_displayer_up)

        print('done!')

    def read_simulation_from_h5(self):
        """
        Reads a simulation from the HDF5 file based on the given parameters, including the gap object.
        """
        with h5py.File(self.h5_file, "r") as f:
            # Check if the simulation exists in the file
            if self.param_hash not in f:
                raise ValueError(
                    f"Simulation with the given parameters and geometry not found in the HDF5 file."
                )

            # Retrieve stored simulation data
            group = f[self.param_hash]

            # Retrieve the class name (needed to instantiate the gap object)
            gap_class_name = group["gap_class"][()].decode("utf-8")

            # Dynamically retrieve the class (assuming it's already imported)
            gap_class = globals().get(gap_class_name)

            if gap_class is None:
                raise ValueError(
                    f"Class {gap_class_name} not found. Please make sure the class is imported."
                )

            # Retrieve parameters (common parameters as a string)
            self.gap.parameters = ast.literal_eval(
                group["parameters"][()].decode("utf-8")
            )

            # Retrieve geometry-specific parameters and initialize the gap object
            geometry_params = ast.literal_eval(
                group["geometry_parameters"][()].decode("utf-8")
            )

            # Initialize the gap object with geometry-specific parameters
            self.gap = gap_class(self.gap.parameters, **geometry_params)

            # Now, set the simulation results (attributes that are not part of the constructor)
            self.gap.npart = group["npart"][()]
            self.gap.gapinteraction = group["gapinteraction"][()]
            self.gap.set_h_up(group["h_up"][()])
            self.gap.set_h_low(group["h_low"][()])
            self.gap.average_h = group["average_h"][()]

            # Optionally, load additional data
            self.gap.gap_volume = group["gap_volume"][()]
            self.gap.particles_volume = group["particles_volume"][()]
            self.gap.vpart_over_vgap = group["vpart_over_vgap"][()]
            self.gap.k_tracker = group["k_tracker"][()]
            self.gap.filling_displayer_low = group["filling_displayer_low"][()]
            self.gap.filling_displayer_up = group["filling_displayer_up"][()]

            # Regenerate hash based on the gap parameters and geometry type
            self.param_hash = self.generate_param_hash()
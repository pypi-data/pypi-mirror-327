from abc import ABC, abstractmethod
from typing import TypedDict
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ossobuco.utils import myplot


class GapParams(TypedDict, total=False):
    xmin: float
    xmax: float
    num_points: int
    hprod: float
    interaction_touch: float
    seed: int
    active_sites_density: float


def sample_indices(x, density):
    """Returns randomly selected indices based on active sites density."""
    n = len(x)
    if density == 1:
        return np.arange(n)  # All indices
    elif density == 0:
        print("Warning: active sites density is 0")
        return np.array([0])  # Return empty array
    else:
        num_points = int(n * density)
        return np.random.choice(np.arange(n), size=num_points, replace=False)  # Random selection


class Gap(ABC):
    """Simulates the filling of a gap between two surfaces with discrete particles."""

    def __init__(self, parameters: GapParams = None):
        """Initializes parameters and sets up the gap configuration."""
        
        # Handle default parameters
        default_params = self.default_params()
        if parameters is None:
            parameters = default_params
        else:
            parameters = {**default_params, **parameters}

        self.parameters = parameters
        self.xmin = parameters.get("xmin", 0)
        self.xmax = parameters.get("xmax", 1)
        self.num_points = parameters.get("num_points", 100)
        self.active_sites_density = parameters.get("active_sites_density", 1)

        self.x = np.linspace(self.xmin, self.xmax, self.num_points)
        self.active_indices = sample_indices(self.x, self.active_sites_density)

        self.hprod = parameters.get("hprod", 1.0)
        self.wprod = (self.xmax - self.xmin) / self.num_points
        self.single_part_volume = self.hprod * self.wprod

        self.interaction_touch = parameters.get("interaction_touch", 1)
        self.seed = parameters.get("seed", 1)

        # Initialize result tracking lists
        self.npart = [0]
        self.gapinteraction = [0]
        self.k_tracker = []
        self.average_h = [0]
        self.filling_displayer_up = None
        self.filling_displayer_low = None

        # For calculating volumes
        self.particles_volume = None
        self.gap_volume = None
        self.vpart_over_vgap = None

    @property
    @abstractmethod
    def h_up(self):
        """Abstract method to define the upper surface geometry."""
        pass

    @property
    @abstractmethod
    def h_low(self):
        """Abstract method to define the lower surface geometry."""
        pass

    @abstractmethod
    def set_geometry(self):
        """Abstract method to set the gap's geometry."""
        pass

    def default_params(self) -> GapParams:
        """Returns default simulation parameters."""
        return {
            "xmin": 0,
            "xmax": 1,
            "num_points": 100,
            "hprod": 0.05,
            "interaction_touch": 1,
            "seed": 1,
            "active_sites_density": 1,
        }

    def show_geometry(self, ax=None, color=None, vlines=True):
        """Visualizes the gap geometry."""
        if ax is None:
            fig, ax = plt.subplots()

        if color is None:
            color = "0.6"

        ax.plot(self.x, self.h_up, marker="x", label=r"$h_{up}$", c="0.3", alpha=0.2)
        ax.plot(self.x, self.h_low, marker="x", label=r"$h_{low}$", c="0.3", alpha=0.2)
        ax.fill_between(np.sort(self.x), self.h_up, color="0.5", alpha=0.5)

        if vlines:
            ax.vlines(self.x, self.h_low, self.h_up, color=color, label=r"D(x)", lw=1)

        ax.scatter(self.x[self.active_indices], self.h_up[self.active_indices], marker="o", c="k")
        ax.scatter(self.x[self.active_indices], self.h_low[self.active_indices], marker="o", c="k")

        ax.set_xlabel("x")
        ax.set_ylabel("h(x)")

    def compute_gap_volume(self):
        """Computes the gap volume using the trapezoidal rule."""
        dx = np.diff(self.x)
        gaps_list = self.h_up - self.h_low
        gap_height = (gaps_list[:-1] + gaps_list[1:]) / 2
        return [np.sum(gap_height * dx)]

    def fill(self):
        # set a seed for reproducibility
        random.seed(self.seed)

        # initialise number of particles and current gap interaction
        n_part = 0
        gap_interaction = 0

        # initialise an interaction tracker, has len(x) and starts with zeroes only
        # at each x position it will keep track of the contribution of gap(x) towards the total interaction
        interaction_tracker = np.zeros(len(self.x))

        d_updt = self.h_up - self.h_low
        d_sum = sum(d_updt[self.active_indices])
        h_tracker = np.zeros(len(self.x))

        h_up_gif = copy.deepcopy(self.h_up)
        h_low_gif = copy.deepcopy(self.h_low)

        self.filling_displayer_up = [np.array(h_up_gif)]
        self.filling_displayer_low = [np.array(h_low_gif)]

        # while gap not full
        THRESHOLD = self.hprod * 1e-6
        while d_sum > THRESHOLD:
            # pick a surface at random, 1 is low, 2 is up
            k = random.randint(1, 2)

            rnd_idx = random.choice(self.active_indices)

            d_chosen_x = d_updt[rnd_idx]

            # if I can still place particles at this x position
            if d_chosen_x > 0:

                # you can still place a particle, so you'll have to display it
                # track the surface to display
                self.k_tracker.append(k)

                # update filling displayer, 1 is low, 2 is up
                if k == 1:
                    h_low_gif[rnd_idx] += self.hprod
                elif k == 2:
                    h_up_gif[rnd_idx] -= self.hprod

                l = np.array(h_low_gif)  # get value not address in memory lol
                self.filling_displayer_low.append(l)

                m = np.array(h_up_gif)  # get value not address in memory lol
                self.filling_displayer_up.append(m)

                # add the size of a particle
                d_chosen_x -= self.hprod
                diff = self.hprod

                # track average height
                h_tracker[rnd_idx] += self.hprod

                # unefficient way of getting average height
                dummy_average = []
                dummy_gap = self.h_up - self.h_low
                # dummy_heights = dummy_gap - h_tracker
                for i, elem in enumerate(dummy_gap):
                    if dummy_gap[i] - h_tracker[i] > 0:
                        dummy_average.append(h_tracker[i])
                self.average_h.append(np.average(dummy_average))

                # count the added particle
                n_part += 1
                self.npart.append(n_part)

                # regarding the interaction to count, depends if you bridged the gap or not
                # if you bridged the gap, add a touch interaction
                if d_chosen_x <= 0:
                    # set distance to zero and update gaps list
                    diff = d_updt[rnd_idx]
                    d_chosen_x = 0
                    d_updt[rnd_idx] = d_chosen_x

                    interaction_tracker[rnd_idx] = self.interaction_touch

                    # compute and update total gap interaction
                    gap_interaction = sum(interaction_tracker)

                    # update gap interaction list for plot
                    self.gapinteraction.append(gap_interaction)

                    d_sum -= abs(diff)

                # if you are not close to bridging, just add a particle
                else:
                    # compute and update total gap interaction
                    gap_interaction = sum(interaction_tracker)

                    # update gap interaction list for plot
                    self.gapinteraction.append(gap_interaction)

                    # update gaps list
                    d_updt[rnd_idx] = d_chosen_x

                    # faaaaast
                    d_sum -= abs(diff)
        
        self.extract_results()

    def extract_results(self):
        self.npart = np.array(self.npart)
        self.gapinteraction = np.array(self.gapinteraction)
        self.gap_volume = self.compute_gap_volume()
        self.particles_volume = np.array(self.npart) * self.single_part_volume
        self.vpart_over_vgap = self.particles_volume / self.gap_volume
        self.k_tracker = self.k_tracker
        self.filling_displayer_low = np.array(self.filling_displayer_low)
        self.filling_displayer_up = np.array(self.filling_displayer_up)
        
        for i in range(1, len(self.average_h)):
            if np.isnan(self.average_h[i]):
                self.average_h[i] = self.average_h[i-1]
        self.average_h = np.array(self.average_h)


    def show_output(self, fig=None, axes: tuple = None, tstep_show: int = None):

        if fig is None and axes is None:
            fig, axes = plt.subplots(1, 3, figsize=(9, 3))

        self.show_geometry(ax=axes[0])
        self.plot_gap_interaction(ax=axes[1])
        self.display_gap_at_timestep(ax=axes[2], timestep=tstep_show)

        plt.tight_layout()
        plt.show()

    def plot_gap_interaction(
        self, ax=None, norm="both", fit=None, label=None, **kwargs
    ):

        if ax is None:
            fig, ax = plt.subplots()

        if norm == None:
            x = np.array(self.npart)
            y = np.array(self.gapinteraction)
            xlabel = "number of particles added"
            ylabel = "gap interaction"

        elif norm == "x":
            x = self.particles_volume / self.gap_volume
            xlabel = "Vpart / Vgap"

            y = np.array(self.gapinteraction)
            ylabel = "gap interaction"

        elif norm == "y":
            x = np.array(self.npart)
            xlabel = "number of particles added"

            max_interaction = self.num_points * self.interaction_touch
            y = np.array(self.gapinteraction) / max_interaction
            ylabel = "gap interaction / max gap interaction"

        elif norm == "both":
            x = self.particles_volume / self.gap_volume
            xlabel = "Vpart / Vgap"
            max_interaction = self.num_points * self.interaction_touch
            y = np.array(self.gapinteraction) / max_interaction
            ylabel = " normalized gap interaction"

        else:
            raise ValueError(
                f"Invalid value for norm: {norm}. Expected None, 'x', or 'y'."
            )

        myplot(ax=ax, x=x, y=y, label=label, **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if label:
            ax.legend()

    def display_gap_at_timestep(
        self,
        ax=None,
        timestep: int = None,
        color: str = None,
        alpha: float = None,
        ybounds: list = None,
        verbose: bool = True,
    ):

        if ax is None:
            fig, ax = plt.subplots()

        max_timesteps = len(self.k_tracker)

        if timestep is None:
            timestep = int(max_timesteps / 2)

        if color is None:
            color = "0.7"

        if alpha is None:
            alpha = 1

        if ybounds is None:
            if max(abs(self.h_low)) == 0:
                lower_bound = -max(self.h_up) * 0.3
            else:
                lower_bound = -max(abs(self.h_low)) * 1.5
            upper_bound = max(self.h_up) * 1.5

            ybounds = [lower_bound, upper_bound]

        ax.plot(self.x, (self.h_up), c="0.3")
        ax.plot(self.x, (self.h_low), c="0.3")

        # plot cement surfaces - grey
        ax.fill_between(np.sort(self.x), (self.h_up), ybounds[1], color="0.5")
        ax.fill_between(np.sort(self.x), (self.h_low), ybounds[0], color="0.5")

        # print max number of timesteps
        max_timesteps = len(self.k_tracker)

        if verbose:
            print(
                f"max number of timesteps = {max_timesteps}\ndefault show displays half simulation = tstep {max_timesteps//2}"
            )

        if timestep > max_timesteps or timestep < 0:
            timestep = max_timesteps

        ax.fill_between(
            np.sort(self.x),
            (self.h_low),
            (self.filling_displayer_low[timestep]),
            color=color,
            alpha=alpha,
        )
        ax.fill_between(
            np.sort(self.x),
            (self.h_up),
            (self.filling_displayer_up[timestep]),
            color=color,
            alpha=alpha,
        )

        # plot cement surfaces - grey again, to mask products overshoot
        ax.fill_between(np.sort(self.x), (self.h_up), ybounds[1], color="0.5")
        ax.fill_between(np.sort(self.x), (self.h_low), ybounds[0], color="0.5")

        # # uncomment if you want contour of products
        # ax.plot(np.sort(self.x), (self.filling_displayer_low[tstep]), color='0.2', alpha=0.3)
        # ax.plot(np.sort(self.x), (self.filling_displayer_up[tstep]), color='0.2', alpha=0.3)

        # plt.tight_layout()
        # plt.show()
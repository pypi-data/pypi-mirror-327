import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Optional, Callable

from ossobuco import Simulation, Displayer
from ossobuco.utils import myplot

class Analyzer(Displayer):
    def __init__(self, simulation: Simulation):
        super().__init__(simulation)
        """
        Initialize the Analyzer with simulation data.

        :param simulation: A Simulation object containing the simulation data
        """
        self.simulation = simulation
        self.npart = simulation.gap.npart
        self.gapinteraction = simulation.gap.gapinteraction

    def plot_data(self, ax: Optional[plt.Axes] = None, label: Optional[str] = None, **kwargs):
        """
        Plot the npart vs gapinteraction data.

        :param ax: Optional axis to plot on (if None, creates a new figure)
        :param label: Optional label for the plot
        """
        if ax is None:
            fig, ax = plt.subplots()

        myplot(ax=ax, x=self.npart, y=self.gapinteraction, label=label, **kwargs)
        ax.set_xlabel("Number of Particles Added (npart)")
        ax.set_ylabel("Gap Interaction (gapinteraction)")

        if label:
            ax.legend()

        plt.tight_layout()

    def plot_normalized_data(self, ax: Optional[plt.Axes] = None, **kwargs):
        """
        Plot the normalized gap interaction against npart (normalized by maximum values).

        :param ax: Optional axis to plot on (if None, creates a new figure)
        """
        if ax is None:
            fig, ax = plt.subplots()

        # Normalize data by the max values
        vpart_norm = self.simulation.gap.vpart_over_vgap 
        gapinteraction_norm = self.gapinteraction / np.max(self.gapinteraction)

        myplot(ax=ax, x=vpart_norm, y=gapinteraction_norm, **kwargs)
        ax.set_xlabel("V part / V gap")
        ax.set_ylabel("Normalized Gap Interaction")

        plt.tight_layout()

    def fit_data(self, model: Callable, p0: Optional[np.ndarray] = None):
        """
        Fit the gapinteraction vs npart data to a model function.

        :param model: A callable model function to fit
        :param p0: Initial guess for the fitting parameters
        :return: popt (fitted parameters), pcov (covariance matrix)
        """
        popt, pcov = curve_fit(model, self.npart, self.gapinteraction, p0=p0)
        return popt, pcov

    def plot_fitted_data(self, model: Callable, popt: np.ndarray, ax: Optional[plt.Axes] = None, label: Optional[str] = None, **kwargs):
        """
        Plot the data along with a fitted curve.

        :param model: The model function that was used to fit the data
        :param popt: Fitted parameters from curve_fit
        :param ax: Optional axis to plot on (if None, creates a new figure)
        :param label: Optional label for the plot
        """
        if ax is None:
            fig, ax = plt.subplots()

        # Plot the raw data
        self.plot_data(ax=ax, label=label, **kwargs)

        # Plot the fitted curve
        x_fit = np.linspace(np.min(self.npart), np.max(self.npart), 1000)
        y_fit = model(x_fit, *popt)
        myplot(ax=ax, x=x_fit, y=y_fit, **kwargs)

        plt.tight_layout()

    def plot_residuals(self, model: Callable, popt: np.ndarray, ax: Optional[plt.Axes] = None):
        """
        Plot the residuals of the data (difference between data and model).

        :param model: The model function used to fit the data
        :param popt: Fitted parameters from curve_fit
        :param ax: Optional axis to plot on (if None, creates a new figure)
        """
        if ax is None:
            fig, ax = plt.subplots()

        # Calculate the residuals
        residuals = self.gapinteraction - model(self.npart, *popt)

        ax.plot(self.npart, residuals, label="Residuals", color="purple")
        ax.axhline(0, color="black", linestyle="--")
        ax.set_xlabel("Number of Particles Added (npart)")
        ax.set_ylabel("Residuals")

        plt.tight_layout()

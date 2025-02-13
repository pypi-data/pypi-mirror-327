# ossobuco

**Ossobuco** is a python library to simulate the growth of products in the gap between two arbitrary surfaces.
It was developed to study the strengthening of contact points between two cement grains as occurs during early-age structural build-up in fresh cement pastes ([Michel et al. 2024](https://www.sciencedirect.com/science/article/pii/S0008884624002461)).

![Demo](assets/gif.gif)


## Installation

`ossobuco` can be installed with pip

```bash
pip install ossobuco
```


## Usage

The `ossobuco` package provides a simulation framework for modeling the filling of a `Gap` between two surfaces with discrete particles. It supports various gap geometries, including `Flat`, `Keil`, `Parabola`, `Sphere`, `Sinusoidal`, `Fish`, and `RandomSurface`.

### Basic Usage

```python
# import needed geometries (example with Keil)
from ossobuco.geometries import Keil

# create gap
gap = Keil(parameters={'hprod':0.01})

# display geometry (optional)
gap.show_geometry()

# perform simulation (fill gap with products)
gap.fill()

# show simulation output (normalized interaction vs. vprod/vgap)
gap.show_output()
```

### Default Simulation Parameters

The following parameters define the gap structure and filling behavior:

- **`xmin`**: `0.0` – Minimum x-boundary.
- **`xmax`**: `1.0` – Maximum x-boundary.
- **`num_points`**: `100` – Number of discrete points in the gap.
- **`hprod`**: `0.1` – Height of each discrete particle added.
- **`interaction_touch`**: `1.0` – Interaction increment upon bridging.
- **`seed`**: `1` – Random seed for reproducibility.
- **`active_sites_density`**: `1.0` – Fraction of surface sites active for product growth.


### Available Gap Geometries

<img src="assets/geometries_png/all_geoms.png" width="1000">

The `ossobuco` package provides various predefined gap geometries:

<details>
  <summary><strong>Flat</strong></summary>

  - **Parameters**:
    - `altitude`: `0.5`

  <img src="assets/geometries_png/flat.png" width="200">
</details>

<details>
  <summary><strong>Keil</strong></summary>

  - **Parameters**:
    - `slope`: `1`
    - `altitude`: `0`

  <img src="assets/geometries_png/keil.png" width="200">
</details>

<details>
  <summary><strong>Parabola</strong></summary>

  - **Parameters**:
    - `radius`: `0.5`
    - `altitude`: `0`

  <img src="assets/geometries_png/parabola.png" width="200">
</details>

<details>
  <summary><strong>Sphere</strong></summary>

  - **Parameters**:
    - `radius`: `0.5`
    - `altitude`: `0`

  <img src="assets/geometries_png/sphere.png" width="200">
</details>

<details>
  <summary><strong>Sinusoidal</strong></summary>

  - **Parameters**:
    - `amplitude`: `0.25`
    - `phi`: `0`
    - `altitude`: `0.5`
    - `wavelength`: `10`

  <img src="assets/geometries_png/sinusoidal.png" width="200">
</details>

<details>
  <summary><strong>Fish</strong></summary>

  - **Parameters**:
    - `body_amplitude`: `1`
    - `body_frequency`: `3.5`
    - `body_offset`: `0`
    - `tail_length`: `0.2`
    - `tail_height`: `1.5`

  <img src="assets/geometries_png/fish.png" width="200">
</details>

<details>
  <summary><strong>RandomSurf</strong></summary>

  - **Parameters**:
    - `altitude`: `0.5`
    - `stdev`: `0.1`
    - `smooth_factor`: `1`
    - `seed_surface`: `1`

  <img src="assets/geometries_png/random_surface.png" width="200">
</details>


### Running a simulation

The `gap.fill` method simulates the filling of a gap between two surfaces with discrete particles. As particles are added to the gap, the following quantities are computed and tracked:

<details>
<summary> npart (Number of Particles)</summary>
Tracks the total number of particles added to the gap. Updated at each timestep when a particle is added.
</details>

<details>
<summary> gapinteraction (Gap Interaction)</summary>
Represents the total interaction between the two surfaces as particles are added. Updated during each timestep, reflecting the change in surface interaction as particles fill the gap. The interaction is computed based on whether a particle bridges the gap or simply fills the space.
</details>

<details>
<summary> d_updt (Gap Height Changes)</summary>
Stores the difference in height (`h_up - h_low`) at each position in the gap. Updated continuously as particles are added to the surfaces.
</details>

<details>
<summary> h_tracker (Height Tracking)</summary>
Tracks the total height added at each `x` position by the particles. Used for calculating the average height of the gap over time.
</details>

<details>
<summary> average_h (Average Height)</summary>
Stores the average gap height after each timestep. Calculated as the average of all non-zero height changes across the gap.
</details>

<details>
<summary> filling_displayer_up & `filling_displayer_low`</summary>
Hold snapshots of the upper and lower surface heights at different timesteps. Updated as particles are added to the gap, showing the progression of the filling process.
</details>

<details>
<summary> gap_volume</summary>
Computed using the `compute_gap_volume` method after the gap is filled. Represents the total volume of the gap at the current timestep.
</details>

<details>
<summary> particles_volume</summary>
The total volume occupied by the particles. Calculated as the number of particles added multiplied by the volume of a single particle.
</details>

<details>
<summary> vpart_over_vgap (Particle-to-Gap Volume Ratio)</summary>
The ratio of the total particle volume to the gap volume. Updated after every particle addition.
</details>

<details>
<summary> interaction_tracker</summary>
Keeps track of the interaction at each `x` position in the gap. Updated each time a particle is added, reflecting whether the particle bridges the gap.
</details>

These quantities are crucial for understanding the dynamics of the gap-filling process, including how particles affect the gap's volume and the interaction between the two surfaces.

### Methods for Visualization

<details>
<summary> show_geometry</summary>
Visualizes the gap geometry with upper and lower surfaces, the gap area, and active sites.  
**Arguments**: `ax`, `color`, `vlines`  
**Displays**: Surface heights and gap area.
</details>

<details>
<summary> plot_gap_interaction</summary>
Plots the relationship between the number of particles added and the gap interaction.  
**Arguments**: `ax`, `norm`, `label`  
**Displays**: Gap interaction vs. particle count or volume ratio.
</details>

<details>
<summary> display_gap_at_timestep</summary>
Shows the gap at a specific timestep, including surface heights and particle filling.  
**Arguments**: `ax`, `timestep`, `color`, `alpha`, `ybounds`  
**Displays**: Gap at a given timestep.
</details>

<details>
<summary> show_output</summary>
Combines visualizations from `show_geometry`, `plot_gap_interaction`, and `display_gap_at_timestep` into a single output.  
**Arguments**: `fig`, `axes`, `tstep_show`  
**Displays**: All relevant plots in one figure.
</details>


### Interaction with .h5 files

The `Simulation`, `Reader`, and `Analyzer` classes allow to store simulation results/retrieve simulatons from .h5 files.

Store simulations in my_h5_file.h5:

```python
from ossobuco.geometries import *
from ossobuco import Simulation

hprod = [0.01, 0.1]

geometries = [Keil, Sphere]

for hp in hprod:
    for geom in geometries:
        gap = geom({"hprod":hp})
        sim = Simulation(gap=gap, h5_file='my_h5_file', OVERWRITE=False)
        sim.run(show_output=False)
```

Read and analyze simulations from my_h5_file.h5:

```python
import matplotlib.pyplot as plt
from ossobuco import Reader, Analyzer

read = Reader(h5_file='jeudi_matin')

keils = read.get_simulations({"gap_class":"Keil"})
spheres = read.get_simulations({"gap_class":"Sphere"})

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,6))

for sim in keils:
    ana = Analyzer(sim)
    ana.plot_normalized_data(ax=ax1, label=ana.simulation.gap.hprod)
    ana.simulation.gap.display_gap_at_timestep(verbose=False, ax=ax3)

for sim in spheres:
    ana = Analyzer(sim)
    ana.plot_normalized_data(ax=ax2, label=ana.simulation.gap.hprod)
    ana.simulation.gap.display_gap_at_timestep(verbose=False, ax=ax4)

ax1.set_title('keil')
ax2.set_title('sphere')

for ax in [ax1, ax2]:
    ax.set_yscale('log')
    ax.legend(title='hprod')

plt.tight_layout()
```

### Algorithm
We define two discretized surfaces (upper and lower), $h_{up}$ and $h_{low}$. The gap is defined as $D(x) = h_{up}(x) - h_{low}(x)$. 

We then grow products between the surfaces by reducing $D(x)$ by $h_{prod}$:

$$ D_i(x)_{new} = D_i(x)_{current} - h_{prod}$$

for randomly picked $x$.

We increment the interaction by 1 unit whenever $D_i = 0$, until the gap is fully filled.



## License

Copyright &copy; 2024 ETH Zurich (Luca Michel)

**Ossobuco** is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

**Ossobuco** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with **Ossobuco**.  If not, see <https://www.gnu.org/licenses/>.
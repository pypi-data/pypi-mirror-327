import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
from IPython.display import clear_output, display  # For notebook display

from ossobuco import Simulation

class Displayer:
    def __init__(self, simulation):
        """
        Initializes the Displayer class with a simulation object.

        :param simulation: The Simulation object containing the data.
        """
        self.simulation = simulation
        self.h5_file = simulation.h5_file
        self.param_hash = simulation.param_hash
        self.gif_name = f"{self.param_hash[:8]}.gif"


    def write_gif(self):
        print(f"Generating GIF {self.gif_name} in {self.h5_file}...")
        print(f"{self.simulation.gap.gap_class}, num_points {self.simulation.gap.num_points}, hprod {self.simulation.gap.hprod}")
        self._generate_gif_on_disk()
        self._save_gif_in_h5()   

    def _generate_gif_on_disk(self, 
                     interval=400,
                     repeat_delay=1200,
                     ):
        """
        Generate a GIF for the simulation, save it, and display it.

        :param output_filename: Output file for the GIF.
        :param interval: Time interval between frames (ms).
        :param repeat_delay: Time before the GIF repeats (ms).
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4))

        max_timesteps = len(self.simulation.gap.k_tracker) + 1

        def update(frame):
            ax1.clear()
            ax2.clear()

            # Plot gap filling on ax1
            ax1.plot(self.simulation.gap.x, self.simulation.gap.h_up, c="0.3")
            ax1.plot(self.simulation.gap.x, self.simulation.gap.h_low, c="0.3")

            if max(abs(self.simulation.gap.h_low)) == 0:
                lower_bound = -max(self.simulation.gap.h_up) * 0.3
            else:
                lower_bound = -max(abs(self.simulation.gap.h_low)) * 1.5
            upper_bound = max(self.simulation.gap.h_up) * 1.5

            ybounds = [lower_bound, upper_bound]

            # plot cement surfaces - grey
            ax1.fill_between(np.sort(self.simulation.gap.x), (self.simulation.gap.h_up), ybounds[1], color="0.5")
            ax1.fill_between(np.sort(self.simulation.gap.x), (self.simulation.gap.h_low), ybounds[0], color="0.5")

            ax1.fill_between(np.sort(self.simulation.gap.x),
                             self.simulation.gap.h_low,
                             self.simulation.gap.filling_displayer_low[frame],
                             color="0.7")
            ax1.fill_between(np.sort(self.simulation.gap.x),
                             self.simulation.gap.h_up,
                             self.simulation.gap.filling_displayer_up[frame],
                             color="0.7")

            ax1.fill_between(np.sort(self.simulation.gap.x), (self.simulation.gap.h_up), ybounds[1], color="0.5")
            ax1.fill_between(np.sort(self.simulation.gap.x), (self.simulation.gap.h_low), ybounds[0], color="0.5")

            # Plot n vs j on ax2
            ax2.plot(self.simulation.gap.npart[0:frame + 1],
                     self.simulation.gap.gapinteraction[0:frame + 1])
            ax2.set_xlim(-1, 1.05 * max(self.simulation.gap.npart))
            ax2.set_ylim(-2, 1.05 * max(self.simulation.gap.gapinteraction))
            ax2.set_xlabel("Number of particles added")
            ax2.set_ylabel("Gap interaction")

            fig.suptitle(f"Timestep {frame}/{max_timesteps - 1}")

            plt.tight_layout()

        # Create the animation with a lower interval (increase interval for slower speed)
        animation = FuncAnimation(
            fig, update, frames=max_timesteps, interval=interval, repeat=False, repeat_delay=repeat_delay
        )

        # Save the animation as a GIF (use Pillow writer as fallback if ImageMagick is not available)
        try:
            animation.save(self.gif_name, writer="imagemagick")
        except Exception as e:
            # print("Imagemagick not found, using Pillow to save GIF.")
            animation.save(self.gif_name, writer="pillow")

        print(f"Generated GIF {self.gif_name}")

        plt.close(fig)  # Close the figure after saving to avoid memory leaks



    def _save_gif_in_h5(self):
        """
        Saves the frames of a GIF .gif on disk into an existing group in an HDF5 file.
        """
        # Check if the GIF already exists before opening it
        try:
            gif = Image.open(self.gif_name)
        except FileNotFoundError:
            print(f"Error: GIF file '{self.gif_name}' not found.")
            return

        # Prepare a list to hold frames as numpy arrays
        frames = []

        # Get the size of the first frame (to make all frames the same size)
        width, height = gif.size

        # Loop through the frames of the GIF
        while True:
            # Convert each frame to RGB (to ensure consistent channels)
            frame = gif.convert('RGB')
            frame = frame.resize((width, height))  # Resize to the first frame's size if needed

            # Convert the frame to a numpy array and append to the frames list
            frames.append(np.array(frame))

            # Check if there are more frames
            try:
                gif.seek(gif.tell() + 1)
            except EOFError:
                break

        # Convert frames list into a numpy array (shape: num_frames x height x width x channels)
        frames = np.array(frames)

        # Open the HDF5 file in append mode
        with h5py.File(self.h5_file, 'a') as f:
            # Check if the group exists, and create it if not
            if self.param_hash not in f:
                f.create_group(self.param_hash)

            # Check if the 'gif_frames' dataset already exists
            group = f[self.param_hash]
            if 'gif_frames' in group:
                print(f"Dataset 'gif_frames' already exists in {self.h5_file}. Overwriting.")
                del group['gif_frames']  # Optionally delete the old dataset

            # Create the dataset inside the specified group
            group.create_dataset('gif_frames', data=frames)

        print(f"GIF saved to group '{self.param_hash}' in {self.h5_file}")



    def display_existing_gif(self):
        """
        Displays the GIF stored in the HDF5 file.
        """
        with h5py.File(self.h5_file, 'r') as f:
            group = f.get(self.param_hash, None)
            if group and 'gif_frames' in group:
                frames = group['gif_frames'][:]
            else:
                print(f"No GIF found for simulation in group '{self.param_hash}'.")

        # Convert frames to uint8 (in case they are not already)
        frames = frames.astype(np.uint8)

        # Create an animated GIF using matplotlib
        fig, ax = plt.subplots()
        ax.axis('off')  # Hide the axis for clean display

        # Create an empty image object for displaying the frames
        img = ax.imshow(frames[0])

        def update_frame(i):
            """Update the image object for each frame."""
            img.set_data(frames[i])
            return [img]

        # Create the animation (blit=True for faster animation)
        anim = FuncAnimation(fig, update_frame, frames=len(frames), interval=100, blit=True)

        # Display the animation inline in Jupyter notebook
        for i in range(len(frames)):
            img.set_data(frames[i])
            display(fig)
            clear_output(wait=True)  # Clear the previous frame
            plt.pause(0.1)  # Pause for a short interval to create animation effect

        plt.close(fig)  # Close the plot after the loop ends


    def display_gif_at_timestep(self, timestep=None):
        """
        Displays the GIF frame at the given timestep (i.e., the `timestep`-th frame).
        """
        with h5py.File(self.h5_file, 'r') as f:
            group = f.get(self.param_hash, None)
            if group and 'gif_frames' in group:
                frames = group['gif_frames'][:]
            else:
                print(f"No GIF found for simulation in group '{self.param_hash}'", flush=True)
                return None
        
        # Convert frames to uint8 (in case they are not already)
        frames = frames.astype(np.uint8)
        
        print(f"max number of timesteps = {len(frames)-1}")

        if timestep is None:
            timestep = len(frames) // 2
            print(f"default displays gap at half simulation, i.e timestep {timestep}")
        # Check if timestep is valid
        if timestep < 0 or timestep >= len(frames):
            timestep = len(frames) - 1

        # Plot the specific frame at the given timestep
        fig, ax = plt.subplots()
        ax.axis('off')  # Hide the axis for clean display
        ax.imshow(frames[timestep])  # Display the i-th frame

        # # Display the frame
        # display(fig)
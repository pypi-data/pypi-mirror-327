from __future__ import annotations

# Std lib
from abc import ABC, abstractmethod
from typing import List, Unpack, Tuple, Literal, Callable, ClassVar, Type

# 3rd party lib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import PathPatch, Circle
from matplotlib.path import Path
from numpy.typing import NDArray
from shapely import Polygon, MultiPolygon, GeometryCollection, unary_union

# Local lib
from .. import shapes
from ..beams import BeamType
from ..mill import Mill
from ..resources import TIMEUNITS, length_units, Material, LENGTHUNITS, time_units
from ..scan_styles.contour import contour

BOUNDARIES = Literal["x_min", "x_max", "y_min", "y_max"]


class FIBInterface(ABC):
    _fov_pixels: ClassVar[int]

    @abstractmethod
    def get_pixelsize(self, units: str) -> float:
        """Returns the pixelsize in the specified units for the current FIB settings."""
        ...

    @abstractmethod
    def get_fov(self, units: str) -> float:
        ...

    @property
    @abstractmethod
    def beam(self) -> BeamType:
        ...


class Add:
    # region Class Body

    _pattern: Pattern

    # endregion Class Body

    # region Dev Methods

    def __init__(self, pattern: Pattern):
        self._pattern = pattern

    # endregion Dev Methods

    # region User Methods

    def rectangle(self, **kwargs: Unpack[shapes.RectangleKwargs]) -> shapes.Rectangle:
        rect = shapes.Rectangle(pattern=self._pattern, **kwargs)  # type: ignore
        self._pattern._add_shape(rect)
        return rect

    def circle(self, **kwargs: Unpack[shapes.CircleKwargs]) -> shapes.Circle:
        circ = shapes.Circle(pattern=self._pattern, **kwargs)  # type: ignore
        self._pattern._add_shape(circ)
        return circ

    def polygon(self, **kwargs: Unpack[shapes.PolyKwargs]) -> shapes.Poly:
        poly = shapes.Poly(pattern=self._pattern, **kwargs)  # type: ignore
        self._pattern._add_shape(poly)
        return poly

    def regular_polygon(self, **kwargs: Unpack[shapes.RegularPolygonKwargs]) -> shapes.RegularPolygon:
        poly = shapes.RegularPolygon(pattern=self._pattern, **kwargs)  # type: ignore
        self._pattern._add_shape(poly)
        return poly

    def lattice(self, **kwargs: Unpack[shapes.LatticeKwargs]) -> shapes.Lattice:
        lattice = shapes.Lattice(pattern=self._pattern, **kwargs)  # type: ignore
        self._pattern._add_shape(lattice)
        return lattice

    # endregion User Methods


class Pattern:

    # region Class Body

    _shapes: List[shapes.Shape]
    _mill: Mill
    _fib: FIBInterface
    _x: float
    _y: float
    _pass_multiplier: int
    _scan_style: Callable
    _material: Material
    Materials: Type[Material]
    add: Add

    __slots__ = ["_shapes", "_mill", "_fib", "_x", "_y", "_pass_multiplier", "add", "_scan_style", "_material",
                 "Materials"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, fib, x: float = 0, y: float = 0) -> None:
        self._fib = fib
        self._shapes = []
        self._mill = Mill()
        self.add = Add(self)
        self.set_position(x, y)
        self._scan_style = contour
        self._material = Material.Default_Si
        self.Materials = Material

    def _add_shape(self, shape: shapes.Shape) -> None:
        self._shapes.append(shape)

    def _get_millable_area(self) -> Polygon | MultiPolygon | GeometryCollection:

        millable = []
        non_millable = []

        def filter_millable(shape_to_filter: shapes.Shape) -> None:
            """Recursively filter all shapes based on the milling flag."""
            if isinstance(shape_to_filter, shapes.CombinedShape):
                for shape in shape_to_filter._shapes:
                    filter_millable(shape)
            elif isinstance(shape_to_filter, shapes.Lattice):
                for row in shape_to_filter._shapes:
                    for shape in row:
                        if shape is not None:
                            filter_millable(shape)
            elif isinstance(shape_to_filter, shapes.Shape):
                if shape_to_filter._millable:
                    millable.append(shape_to_filter.polygon)
                else:
                    non_millable.append(shape_to_filter.polygon)
            else:
                raise TypeError(f"Got '{type(shape_to_filter)}', expected 'Shape' or any of it's subclasses.")
            return

        for pattern_shape in self._shapes:
            filter_millable(pattern_shape)

        millable_area = unary_union(millable)
        non_millable_area = unary_union(non_millable)
        millable_area = millable_area.difference(non_millable_area)

        return millable_area

    def _get_pattern_ax(self, ax: plt.Axes = None, alpha: float = 1) -> plt.Axes:
        """Makes a plot where the millable area is filled in, not including any area containing a non-millable shape."""

        millable_area = self._get_millable_area()

        if ax is None:
            ax = plt.gca()

        if millable_area.is_empty:
            print("No millable area to plot.")
        else:
            if millable_area.geom_type == "MultiPolygon":
                for poly in millable_area.geoms:
                    exterior_coords = np.array(poly.exterior.coords)
                    interiors = [np.array(interior.coords) for interior in poly.interiors]
                    path = Path.make_compound_path(Path(exterior_coords), *[Path(interior) for interior in interiors])
                    patch = PathPatch(path, facecolor='black', edgecolor='none', alpha=alpha, label="Millable")
                    ax.add_patch(patch)
            else:
                poly = millable_area
                exterior_coords = np.array(poly.exterior.coords)
                interiors = [np.array(interior.coords) for interior in poly.interiors]
                path = Path.make_compound_path(Path(exterior_coords), *[Path(interior) for interior in interiors])
                patch = PathPatch(path, facecolor='black', edgecolor='none', alpha=alpha, label="Millable")
                ax.add_patch(patch)

        return ax

    def _pixelate_beam_path(self, streamlines: NDArray) -> NDArray:

        # Conversion factor: nm -> pixels
        conversion_factor = 1 / self._fib.get_pixelsize("nm")

        # Extract physical positions (assuming column 1 = x, column 2 = y)
        streamlines[:, 1] = np.rint(streamlines[:, 1] * conversion_factor)
        streamlines[:, 2] = np.rint(streamlines[:, 2] * conversion_factor)

        return streamlines

    def _get_passes(self, streamlines: NDArray = None) -> int:

        millable_area = length_units(self._get_millable_area().area, "nm", "um", power=2)
        millable_volume = millable_area * self._mill.get_mill_depth("um")
        volume_pr_dose = self._material.value
        time_goal = millable_volume / (self._fib.beam.get_current("na") * volume_pr_dose)

        effective_mill_time = 0
        for vec in streamlines:
            if vec.shape[0] == 4:
                if vec[3] == 0:
                    continue
            effective_mill_time += vec[0]
        effective_mill_time = time_units(effective_mill_time * 100, "ns", "s")

        nr_passes = np.rint(time_goal/effective_mill_time).astype(int)

        return nr_passes

    # endregion Dev Methods

    # region User Methods

    def set_material(self, material: Material) -> None:
        """Sets the material the sample is made out of. Materials can be found under the Materials variable of the
        pattern instance."""
        self._material = material

    def write_stream(self, filename: str) -> None:
        streamlines = np.vstack(self._scan_style(self._get_millable_area(), self._mill, self._fib.beam, rasterize=True))
        streamlines = self._pixelate_beam_path(streamlines)
        passes = self._get_passes(streamlines)

        streamlines[:, 1:3] += np.array([self._fib._fov_pixels // 2, self._fib._fov_pixels // 2])
        if not filename.endswith(".str"):
            filename += ".str"
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(["s16\n", str(streamlines.shape[0]) + "\n", str(passes) + "\n"])
            file.writelines([f"{int(line[0])} {int(line[1])} {int(line[2])}"
                             f"{' ' + str(int(line[3])) + "\n" if line[3] != 2 else '\n'}"
                             for line in streamlines])
        return

    def set_position(self, x: float = 0, y: float = 0) -> None:
        """Sets the position of the pattern, including all contained shapes."""
        self._x, self._y = x, y

    def plot_pattern(self, figsize: Tuple[float, float] = (15, 10), alpha: float = 0.6) -> None:
        """Makes a plot where the millable area is filled in, not including any area containing a non-millable shape."""
        plt.rcParams["figure.figsize"] = figsize
        prev_pos = self._x, self._y
        self.set_position(0, 0)
        ax = self._get_pattern_ax(None, alpha)
        self.set_position(*prev_pos)
        ax.relim()
        ax.autoscale_view()
        ax.set_aspect('equal')
        # Retrieve the current handles and labels
        handles, labels = plt.gca().get_legend_handles_labels()

        # Create a dictionary to remove duplicates. In Python 3.7+, dict preserves insertion order.
        by_label = dict(zip(labels, handles))

        # Now pass the unique handles and labels to plt.legend()
        plt.legend(by_label.values(), by_label.keys())
        plt.show()

    def plot_beam_path(self, figsize: Tuple[float, float] = (15, 10), alpha: float = 0.25, rasterize: bool = True) -> None:

        millable_area = self._get_millable_area()

        lines = self._scan_style(millable_area, self._mill, self._fib.beam, rasterize=rasterize)

        plt.figure(figsize=figsize)
        ax = self._get_pattern_ax(None, alpha)
        for line in lines:
            plt.plot(line[:, 1], line[:, 2], "o-")

        plt.gca().set_aspect("equal")
        plt.show()

    def animate_beam_path(self, figsize=(15, 10), alpha=0.25, repeat: bool = False):
        """
        Animates drawing the beam path contours with fixed axis limits.
        The axis limits are computed from all contour line data so that the
        plot’s size remains constant throughout the animation.
        """

        # Get the overall geometry and compute the contour lines.
        millable_area = self._get_millable_area()
        lines = contour(millable_area, self._mill, self._fib.beam, rasterize=True)

        # Precompute coordinate data for each line.
        # Each entry in line_data is a tuple (x_values, y_values)
        line_data = []
        for line in lines:
            x, y = line[:, 1], line[:, 2]
            line_data.append((list(x), list(y)))

        # Compute the overall bounding box from all lines.
        all_x = [x for (x_vals, _) in line_data for x in x_vals]
        all_y = [y for (_, y_vals) in line_data for y in y_vals]
        margin = 1  # optional extra space around the data
        x_min, x_max = min(all_x) - margin, max(all_x) + margin
        y_min, y_max = min(all_y) - margin, max(all_y) + margin

        # Create the figure and axis with fixed limits.
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect("equal")

        # State dictionary to track animation progress.
        state = {
            'current_line': 0,  # index of the line being drawn
            'current_point': 0,  # index of the next point in the current line
            'drawn_lines': []  # list of completed lines
        }

        # Determine the total number of frames (one per point).
        total_frames = sum(len(x_vals) for (x_vals, _) in line_data)

        beam_radius = self._fib.beam.get_radius("nm")

        def update(frame):
            """
            Update function for FuncAnimation.
            Adds one point to the current line at each frame and then moves on.
            """
            # Update the state: draw one more point on the current line.
            if state['current_line'] < len(line_data):
                x_vals, y_vals = line_data[state['current_line']]
                if state['current_point'] < len(x_vals):
                    state['current_point'] += 1
                else:
                    # Current line is finished; store it and move to next line.
                    state['drawn_lines'].append((x_vals, y_vals))
                    state['current_line'] += 1
                    state['current_point'] = 0

            # Clear the axis and reapply fixed limits.
            ax.clear()
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.set_aspect("equal")

            # Optionally, reapply any background or styling here (e.g., via self._get_pattern_ax).

            # Draw all completed lines (blue).
            for x_vals, y_vals in state['drawn_lines']:
                ax.plot(x_vals, y_vals, alpha=0.3)
            # Draw the current line (partial, in red) if it exists.
            if state['current_line'] < len(line_data):
                x_vals, y_vals = line_data[state['current_line']]
                ax.plot(x_vals[:state['current_point']], y_vals[:state['current_point']], color='red')

                last_x = x_vals[state['current_point'] - 1]
                last_y = y_vals[state['current_point'] - 1]

                # Add a circle with radius 6.5 at the last plotted point
                circle = Circle((last_x, last_y), beam_radius, color='black',
                                fill=True, alpha=0.5, linewidth=0)
                ax.add_patch(circle)

            return []  # When not using blit, returning an empty list is fine.

        # Create the animation.
        anim = FuncAnimation(fig, update, frames=total_frames, interval=10, blit=False, repeat=repeat,
                             cache_frame_data=True)

        plt.show()

    def get_dwell_time(self, units: TIMEUNITS) -> float:
        return self._mill.get_dwell_time(units)

    def set_dwell_time(self, dt: float, units: TIMEUNITS) -> None:
        self._mill.set_dwell_time(dt, units)

    def set_depth(self, depth: float, units: LENGTHUNITS = "um") -> None:
        self._mill.set_mill_depth(depth, units)

    def get_depth(self, units: LENGTHUNITS) -> float:
        return self._mill.get_mill_depth(units)

    def get_overlap(self) -> float:
        return self._mill.get_overlap()

    def set_overlap(self, overlap_fraction: float) -> None:
        self._mill.set_overlap(overlap_fraction)

    def set_pass_multiplier(self, multiplier: int) -> None:
        """ Sets the number of hardcoded passes for the beam path.

            - If set to 1, the beam will trace the pattern once in the exported stream file.
              The number of actual passes performed will then be determined by the "nr. of passes" parameter in the
              stream file or an override in the FIB machine's interface.
            - If set to ie. 2, the beam will trace the pattern twice in the exported stream file.
              This is equivalent to setting the multiplier to 1 and adjusting the "nr. of passes" parameter to 2.

            This feature is particularly useful for parameter sweeps. For example, suppose you need to create two
            versions of the same pattern with different dwell times while using the same stream file.
            To achieve the same milling depth, the number of passes must vary. However, since the stream file
            enforces a single pass setting for the entire file, you can work around this by adjusting
            the pass multiplier.

            For instance, if one pattern has a 1 µs dwell time and another has 0.5 µs, setting the pass multiplier of
            the 0.5 µs pattern to 2 ensures both receive the same dose.
        """
        # assert isinstance(multiplier, int)
        # self._pass_multiplier = multiplier
        raise NotImplementedError(f"This feature is currently not supported. Will be in later versions.")

    def place_next_to(self, pattern: Pattern, boundary: BOUNDARIES, offset: float = 0) -> None:
        """Places the pattern adjacent to the specified boundary of another pattern."""
        direction = -1 if "min" in boundary else 1
        pos = getattr(pattern, boundary) + (getattr(self, f"{boundary[0]}_span") / 2) * direction + offset
        self.set_position(**{boundary[0]: pos})

    # endregion User Methods

    # region Properties

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        self.set_position(x=x)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        self.set_position(y=y)

    @property
    def x_span(self) -> float:
        return self.x_max - self.x_min

    @property
    def y_span(self) -> float:
        return self.y_max - self.y_min

    @property
    def x_min(self) -> float:
        return min([shape.x_min for shape in self._shapes]) + self._x

    @property
    def x_max(self) -> float:
        return max([shape.x_max for shape in self._shapes]) + self._x

    @property
    def y_min(self) -> float:
        return min([shape.y_min for shape in self._shapes]) + self._y

    @property
    def y_max(self) -> float:
        return max([shape.y_max for shape in self._shapes]) + self._y

    # endregion Properties

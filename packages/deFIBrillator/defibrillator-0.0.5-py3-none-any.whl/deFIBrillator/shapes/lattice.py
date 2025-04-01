from __future__ import annotations

# Std lib
import gc
from typing import List, TypedDict, Unpack, Tuple
from copy import copy

# 3rd party lib
import numpy as np
from numpy import array, deg2rad, vstack, column_stack
from numpy.typing import NDArray
from shapely import Polygon, MultiPolygon, unary_union

# Local lib
from .shape import Shape


class LatticeKwargs(TypedDict, total=False):
    x: float
    y: float
    rows: int
    cols: int
    alpha: float
    beta: float
    gamma: float
    rotation: float
    shape: Shape


class CopyKwargs(TypedDict, total=False):
    x: float
    y: float


class Lattice(Shape):

    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"rows": 2, "cols": 2, "alpha": 200, "beta": 200, "gamma": 90})

    # Instance variables
    _sites: NDArray
    _rows: int
    _cols: int
    _alpha: float
    _beta: float
    _gamma: float
    _shapes: List[List[Shape | None]]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, **kwargs: Unpack[LatticeKwargs]) -> None:
        shape = kwargs.pop("shape", None)
        super().__init__(**kwargs)

        self._construct_site_matrix()
        if shape:
            self._create_shapes(shape)

    def _construct_first_unit_cell(self) -> NDArray:
        """
        Create the first unit cell vertices using the unit vectors.
        Returns two rows of vertices:
          - bottom_row: [bottom_left, bottom_right]
          - top_row:    [top_left, top_right]
        Also returns the unit vectors v1 and v2.
        """
        gamma_rad = deg2rad(self._gamma)
        v1 = np.array([self._alpha, 0])
        v2 = np.array([self._beta * np.cos(gamma_rad), self._beta * np.sin(gamma_rad)])

        bottom_left = np.array([0, 0])
        bottom_right = v1
        top_left = v2
        top_right = v1 + v2

        bottom_row = np.array([bottom_left, bottom_right])
        top_row = np.array([top_left, top_right])

        return array([bottom_row, top_row])

    def _construct_site_matrix(self) -> None:
        """Constructs a 2D matrix that contains the coordinates for all lattice sites. Deletes all previous shapes
        and re-initializes the list containg the lattice's shapes where each element is None, allowing assignment
        through indexing later."""

        unit_cell = self._construct_first_unit_cell()
        lattice = unit_cell.copy()

        if self._rows == 1:
            lattice = lattice[0, :]
        elif self._rows == 2:
            pass
        else:
            for i in range(self._rows - 2):
                this_row = lattice[-(2), :].copy() + array([0, unit_cell[1, 0, 1] * 2])
                lattice = vstack((lattice, array([this_row])))

        if self._cols == 1:
            lattice = lattice[:, 0]
        elif self._cols == 2:
            pass
        else:
            for _ in range(self._cols - 2):
                this_col = array([lattice[:, -2].copy() + array([unit_cell[0, 1, 0] * 2, 0])])
                this_col = this_col.transpose(1, 0, 2)
                lattice = column_stack((lattice, array([this_col])[0]))

        lattice -= array([np.max(lattice[:, :, 0]) / 2, np.max(lattice[:, :, 1]) / 2])

        # Delete all shapes contained in the lattice
        if hasattr(self, "_shapes"):
            for row in self._shapes:
                for col in row:
                    del col  # Remove references to objects

            self._shapes.clear()  # Remove references from the list itself
            gc.collect()  # Ensure immediate cleanup

        # Re-initialize indexable list of shapes
        self._shapes = [[None for i in range(lattice.shape[1])] for j in range(lattice.shape[0])]  # type: ignore

        # Assign site matrix to member variable
        self._sites = lattice

    def _create_shapes(self, shape: Shape, rows: Tuple[int, int] = None, cols: Tuple[int, int] = None) -> None:
        """Create a shape at each lattice site. If previously occupied, delete and replace."""
        if rows is None:
            rows = (0, self._sites.shape[0])
        if cols is None:
            cols = (0, self._sites.shape[1])

        # Set the original shape at the first position
        shape.set_position(*self._sites[0, 0])
        skip = True
        for ridx, row in enumerate(self._sites[rows[0]:rows[1]]):
            for cidx, col in enumerate(row[cols[0]:cols[1]]):
                del self._shapes[ridx][cidx]
                if skip:
                    self._shapes[ridx].insert(cidx, shape)
                    skip = False
                    continue
                self._shapes[ridx].insert(cidx, shape.copy(x=col[0], y=col[1]))

    def _get_polygon(self) -> Polygon | MultiPolygon:
        shapes = []
        for row in self._shapes:
            for s in row:
                if s is not None:
                    shapes.append(s.polygon)
        return unary_union(shapes)

    def __getitem__(self, key) -> Lattice:
        """
        Enable indexing and slicing for the Lattice.

        If a two-dimensional slice is used (e.g., lattice[1:3, 2:4]),
        return a new Lattice object containing the corresponding subset of sites.
        If two integer indices are provided (e.g., lattice[i, j]),
        return the site object at that position.
        If only one index is provided, treat it as row indexing and return that row as a list.
        """
        if isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Lattice indexing supports two indices (row, col)")

            row_idx, col_idx = key

            # Handle slices properly
            if isinstance(row_idx, slice) or isinstance(col_idx, slice):
                row_slice = self._shapes[row_idx]  # Select relevant rows

                # Ensure row_slice is always a list of lists
                if isinstance(row_slice, list) and row_slice and not isinstance(row_slice[0], list):
                    row_slice = [row_slice]

                    # Get the subset of sites and return as a new Lattice object
                new_sites = self._sites[row_idx, col_idx]
                if isinstance(row_idx, int) or isinstance(col_idx, int):
                    if isinstance(col_idx, int):
                        shapes = [[row[col_idx]] for row in row_slice]
                    else:
                        shapes = [row[col_idx] for row in row_slice]
                    min_x, max_x = np.min(new_sites[:, 0]), np.max(new_sites[:, 0])
                    min_y, max_y = np.min(new_sites[:, 1]), np.max(new_sites[:, 1])
                else:
                    shapes = [row[col_idx] for row in row_slice]
                    min_x, max_x = np.min(new_sites[:, :, 0]), np.max(new_sites[:, :, 0])
                    min_y, max_y = np.min(new_sites[:, :, 1]), np.max(new_sites[:, :, 1])
                new_pos = (min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2)

            # Single element access
            else:
                shapes = [[self._shapes[row_idx][col_idx]]]
                new_sites = array([[self._sites[row_idx, col_idx]]])
                new_pos = new_sites[0, 0, 0], new_sites[0, 0, 1]

        # If a single integer is provided, return the full row
        elif isinstance(key, int):
            shapes = self._shapes[key]
            new_sites = self._sites[key]
            x_min = np.min(new_sites[:, 0])
            x_max = np.max(new_sites[:, 0])
            new_pos = (x_min + (x_max - x_min) / 2, new_sites[0, 0])
        else:
            raise IndexError(f"Invalid index. Got '{key}'.")

        new_rows, new_cols = new_sites.shape[:2]
        new_lattice = Lattice(rows=2, cols=2)
        new_lattice._rows = new_rows
        new_lattice._cols = new_cols
        new_lattice._pattern = self._pattern
        new_lattice._x, new_lattice._y = new_pos
        new_lattice._sites = new_sites
        new_lattice._shapes = shapes
        return new_lattice

    def __setitem__(self, key, shape: Shape | None):
        """
        Replace shapes in the lattice.

        If a single index (row, col) is provided, replace the shape at that position.
        If a slice is used, the first position is assigned `shape`, and the rest are filled with `shape.copy()`.
        """
        if not isinstance(shape, (Shape, type(None))):  # type: ignore
            raise TypeError(f"Invalid type. Expected type(Shape) or NoneType, got '{type(shape)}'.")
        elif isinstance(shape, Lattice):
            raise TypeError(f"Invalid type. Got '{type(shape)}'. "
                            f"Lattices cannot currently be assigned to points in another lattice.")

        if isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Lattice indexing supports two indices (row, col)")

            row_idx, col_idx = key

            # Handle slices properly
            if isinstance(row_idx, slice) or isinstance(col_idx, slice):
                row_slice = self._shapes[row_idx]  # Select relevant rows

                # Ensure row_slice is always a list of lists
                if isinstance(row_slice, list) and row_slice and not isinstance(row_slice[0], list):
                    row_slice = [row_slice]

                # Apply shape and its copies
                first_set = False
                for i, row in enumerate(self._shapes[row_idx]):
                    for j in range(len(row[col_idx])):
                        # Delete the existing shape
                        delshape = row[col_idx][j]
                        row[col_idx].remove(delshape)
                        del delshape

                        # Assign shape to the first spot, then copy for others
                        if not first_set:
                            row[col_idx].insert(j, shape)
                            first_set = True
                        else:
                            if shape is not None:
                                row[col_idx].insert(j, shape.copy())
                            else:
                                row[col_idx].insert(j, shape)

            else:
                # Delete and replace a single shape
                delshape = self._shapes[row_idx][col_idx]
                self._shapes[row_idx][col_idx] = shape
                del delshape

        else:
            raise IndexError("Invalid index type. Use (row, col) indexing.")


    # endregion Dev Methods

    # region User Methods

    def rotate(self, rot_angle: float, rot_point: Tuple[float, float] | Shape = None) -> rotate:

        # Create the rotation matrix
        theta = np.deg2rad(rot_angle)
        self._sites = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])

        for row, x in zip(self._shapes, self._sites):
            for shape, pos in zip(row, x):
                shape.rotate(rot_angle)
                shape.set_position(*pos)

    def set_position(self, x: float | Shape = None, y: float | Shape = None) -> None:

        old_pos = array([self._x, self._y])

        if x is not None:
            self._x = x
        else:
            x = 0
        if y is not None:
            self._y = y
        else:
            y = 0

        self._sites -= old_pos
        self._sites += array([x, y])

        for row, x in zip(self._shapes, self._sites):
            for shape, pos in zip(row, x):
                shape.set_position(*pos)

    def copy(self, **kwargs) -> Lattice:
        new_lattice = copy(self)
        new_lattice._shapes = [[shape.copy() for shape in row] for row in self._shapes]
        super().copy(**kwargs)
        return new_lattice

    # endregion User Methods

    # region Properties

    @property
    def x(self) -> float:
        """Getter for x coordinates"""
        return self._x

    @x.setter
    def x(self, new_x):
        """Setter for x coordinates. Updates site positions accordingly."""
        self.set_position(x=new_x)

    @property
    def y(self):
        """Getter for y coordinates"""
        return self._y

    @y.setter
    def y(self, new_y):
        """Setter for y coordinates. Updates site positions accordingly."""
        self.set_position(y=new_y)

    # endregion Properties

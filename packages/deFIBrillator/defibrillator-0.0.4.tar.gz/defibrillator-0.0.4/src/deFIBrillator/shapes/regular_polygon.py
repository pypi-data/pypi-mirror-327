from __future__ import annotations

# Std lib
import math
from typing import TypedDict, Unpack

# 3rd party lib
from shapely import Polygon

# Local lib
from .shape import Shape


class RegularPolygonKwargs(TypedDict, total=False):
    millable: bool
    nr_sides: int
    x: float
    y: float
    inner_radius: float
    outer_radius: float
    side_length: float
    rotation: float


class RegularPolygon(Shape):

    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"nr_sides": 6, "outer_radius": 50.})

    # Instance variables
    _nr_sides: int
    _outer_radius: float

    # endregion Class Body

    # region Dev Methods

    def __init__(self, **kwargs: Unpack[RegularPolygonKwargs]):

        nr_sides = kwargs.pop("nr_sides", None)
        if nr_sides is not None:
            if nr_sides < 3:
                raise ValueError(f"The numer of sides of a regular polygon must be greater than 2, got '{nr_sides}'.")
            else:
                self._nr_sides = nr_sides
        else:
            self._nr_sides = self._default_geometry["nr_sides"]

        kwargs["outer_radius"] = self._to_outer_radius(**kwargs)

        super().__init__(**kwargs)

    def _get_polygon(self, **kwargs: Unpack[RegularPolygonKwargs]) -> Polygon:

        # Generate regular polygon vertices
        angles = [90 + i * (360 / self.nr_sides) for i in range(self.nr_sides)]
        points = [
            (self._outer_radius * math.cos(math.radians(angle)),
             self._outer_radius * math.sin(math.radians(angle)))
            for angle in angles
        ]
        polygon = Polygon(points)

        # Apply translation and rotation if needed
        polygon = self._apply_translation(polygon)
        polygon = self._apply_rotation(polygon)

        # Initialize the shape with final polygon
        return polygon

    def _to_outer_radius(self, **kwargs) -> float:

        inner_radius = kwargs.pop("inner_radius", None)
        outer_radius = kwargs.pop("outer_radius", None)
        side_length = kwargs.pop("side_length", None)

        # Validate only one size parameter is provided
        if len([a for a in [inner_radius, outer_radius, side_length] if a is not None]) > 1:
            raise ValueError("Expected either 'inner_radius', 'outer_radius', or 'side_length', got multiple.")

        if inner_radius is not None:
            return inner_radius / math.cos(math.pi / self._nr_sides)  # type: ignore
        elif side_length is not None:
            return side_length / (2 * math.sin(math.pi / self._nr_sides))  # type: ignore
        elif outer_radius is not None:
            return outer_radius  # type: ignore

    # endregion Dev Methods

    # region User Methods

    def copy(self, **kwargs: Unpack[RegularPolygonKwargs]) -> RegularPolygon:
        return super().copy(**kwargs)

    # endregion User Methods

    # region Properties

    @property
    def nr_sides(self) -> int:
        """Returns the polygon's number of sides."""
        return self._nr_sides

    @nr_sides.setter
    def nr_sides(self, nr: int) -> None:
        """Sets the polygon's number of sides."""
        self._nr_sides = nr

    @property
    def side_length(self) -> float:
        """Returns the side lenght of the polygon."""
        return self._outer_radius * (2 * math.sin(math.pi / self._nr_sides))

    @side_length.setter
    def side_length(self, length: float) -> None:
        """Sets the side length og the polygon."""
        self._outer_radius = self._to_outer_radius(side_length=length)

    @property
    def inner_radius(self) -> float:
        """Returns the inner radius of the polygon."""
        return self._outer_radius * math.cos(math.pi / self._nr_sides)

    @inner_radius.setter
    def inner_radius(self, radius: float) -> None:
        """Sets the inner radius of the polygon."""
        self._to_outer_radius(inner_radius=radius)

    @property
    def outer_radius(self) -> float:
        return self._outer_radius

    @outer_radius.setter
    def outer_radius(self, radius: float) -> None:
        """Sets the outer radius of the polygon."""
        self._outer_radius = radius

    # endregion Properties

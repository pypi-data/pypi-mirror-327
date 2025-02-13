from __future__ import annotations

# Std lib
import math
from abc import abstractmethod
from copy import copy
from typing import Tuple, ClassVar, Dict, Any, TypedDict, Unpack, List, Union, Literal, Iterable

# 3rd party lib
from matplotlib import pyplot as plt
from shapely import unary_union
from shapely.affinity import translate, rotate
from shapely.geometry import Polygon, MultiPolygon, Point


# region Constants and Literals

BOUNDARIES = Literal["x_min", "x_max", "y_min", "y_max"]


# endregion Constants and Literals


# region Shape Base Class
class Shape:
    # region Class Body

    # Class variables
    _default_geometry: ClassVar[Dict] = {"x": 0, "y": 0, "rotation": 0, "millable": True}

    # Instance variables
    _x: float
    _y: float
    _rotation: float
    _millable: bool
    _pattern: Any

    __slots__ = ["_x", "_y", "_rotation", "_millable", "_pattern"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, pattern=None, **kwargs) -> None:

        if pattern is not None:
            self._pattern = pattern

        # Use the default values for not passed arguments
        default = self._default_geometry.copy()
        default.update(kwargs)
        for k, v in default.items():
            setattr(self, "_" + k, v)

    def _apply_translation(self, polygon: Polygon) -> Polygon:
        shape = translate(polygon, *self._get_absolute_position())
        return shape

    def _apply_rotation(self, polygon: Polygon) -> Polygon:
        return rotate(polygon, self._rotation)

    def _get_min(self) -> Tuple[float, float]:
        """Returns a tuple of the minimum x and y coordinates."""
        x, y = self.polygon.exterior.xy
        return min(x), min(y)

    def _get_max(self) -> Tuple[float, float]:
        """Returns a tuple of the maximum x and y coordinates."""
        x, y = self.polygon.exterior.xy
        return max(x), max(y)

    def _add_to_pattern(self) -> None:
        """Adds the shape to the provided pattern."""
        if self._pattern is not None:
            self._pattern._add_shape(self)

    def _get_absolute_position(self) -> Tuple[float, float]:
        """Returns the absolute position of the shape, meaning the position of the parent pattern plus the
        position of the shape."""
        if self._pattern is None:
            return self._x, self._y
        else:
            return self._x + self._pattern.x, self._y + self._pattern.y

    @abstractmethod
    def _get_polygon(self) -> Polygon | MultiPolygon:
        ...

    # endregion Dev Methods

    # region User Methods

    def plot(self) -> None:
        plt.figure(figsize=(15, 10))
        polygon = self.polygon
        if polygon.geom_type == "MultiPolygon":
            for poly in polygon.geoms:
                if self._millable:
                    plt.fill(*poly.exterior.xy)
                else:
                    plt.plot(*poly.exterior.xy)
        else:
            if self._millable:
                plt.fill(*polygon.exterior.xy)
            else:
                plt.plot(*polygon.exterior.xy)
        plt.gca().set_aspect("equal")
        plt.show()

    def set_position(self, x: float | Shape = None, y: float | Shape = None) -> None:
        """
        Set position using cartesian coordinates.

        Args:
            x (float | Shape): The new x-coordinate. Uses previous coordinate if not provided.
            y (float): The new y-coordinate. Uses previous coordinate if not provided.
        """
        self._x = x if x is not None else self._x
        self._y = y if y is not None else self._y

    def set_position_polar(self,
                           radius: float,
                           theta: float,
                           origin: tuple[float, float] | Shape = (0.0, 0.0)) -> None:
        """
        Set position using polar coordinates relative to a specified origin

        Args:
            radius: Distance from origin to new position
            theta: Angle in degrees (counterclockwise from positive x-axis)
            origin: Tuple (x, y) specifying the reference point. Can be another shape, then it's position is used.
                    Defaults to (0, 0) if not provided
        """

        # Unpack origin coordinates
        if isinstance(origin, Shape):
            origin_x, origin_y = origin.x, origin.y
        else:
            origin_x, origin_y = origin

        # Convert angle to radians
        theta_rad = math.radians(theta)

        # Convert polar to Cartesian coordinates relative to origin
        x = origin_x + radius * math.cos(theta_rad)
        y = origin_y + radius * math.sin(theta_rad)

        # Update position using existing Cartesian method
        self.set_position(x=x, y=y)

    def set_rotation(self, rot_angle: float) -> None:
        """Sets the counterclockwise rotation of the shape."""
        self._rotation = float(rot_angle)

    def rotate(self, rot_angle: float, rot_point: Tuple[float, float] | Shape = None) -> rotate:
        """Rotates the shape counterclockwise from it's current rotation around a point. If no rotation point is
        provided, the shape is rotated around it's center position. Another shape can be provided as the rotation point.
        The method can be stacked, ie. shape.rotate(45)(36)."""

        self._rotation = self._rotation + rot_angle
        if isinstance(rot_point, Shape):
            rot_point = (rot_point.x, rot_point.y)
        elif rot_point is None:
            rot_point = (self._x, self._y)
        elif not isinstance(rot_point, (tuple, list)):
            raise TypeError(f"Expected iterable type, got '{type(rot_point)}'.")

        point = rotate(Point(self._x, self._y), self._rotation, rot_point)
        self.set_position(point.x, point.y)

        return self.rotate

    def place_next_to(self, boundary: BOUNDARIES, shape: Shape, offset: float = 0) -> None:
        """Places the shape adjacent to the specified boundary of the provided shape."""
        axis = boundary[0]
        scale = -1 if boundary[2:] == "min" else 1
        coordinate = getattr(shape, boundary)
        setattr(self, boundary[0],
                coordinate
                + offset
                + scale
                * ((getattr(self, axis + "_max") - getattr(self, axis + "_min")) / 2)
                )

    @abstractmethod
    def copy(self, **kwargs):
        """Returns an exact copy of the shape, modified according to the provided kwargs."""

        # 'Secret' keyword for not adding copied shape to parent pattern
        add = kwargs.pop("add_to_pattern", True)

        new = copy(self)

        for k, v in kwargs.items():
            setattr(new, "_" + k, v)

        if add:
            new._add_to_pattern()

        return new

    def combine(self, other: Union[Iterable[Union[Shape]], Shape]) -> CombinedShape:
        """
        Combines the shape with other shapes to form a composite shape.
        """

        # Remove shapes from the pattern
        self._pattern._shapes.remove(self)
        if isinstance(other, (list, tuple)):
            for o in other:
                if o in self._pattern._shapes:
                    self._pattern._shapes.remove(o)
        else:
            self._pattern._shapes.remove(other)

        # Extract shapes
        shapes = []

        def extract_shapes(shape: Shape) -> None:
            if isinstance(shape, CombinedShape):
                for subshape in shape._shapes:
                    extract_shapes(subshape)
            elif isinstance(shape, Shape):
                shapes.append(shape)
            elif isinstance(shape, (list, tuple)):
                for s in shape:
                    extract_shapes(s)
            else:
                raise TypeError(f"Expected type 'Shape' or subclass, got '{type(shape)}'.")

        extract_shapes(self)
        extract_shapes(other)

        # Create combined shape and add it to pattern
        combined = CombinedShape(self._pattern)
        combined._shapes = shapes
        combined._add_to_pattern()

        return combined

    # endregion User Methods

    # region Properties

    @property
    def polygon(self) -> Polygon | MultiPolygon:
        """Returns the polygon associated with the shape."""
        return self._get_polygon()

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = float(value)

    @property
    def x_min(self) -> float:
        return self._get_min()[0]

    @property
    def x_max(self) -> float:
        return self._get_max()[0]

    @property
    def y_min(self) -> float:
        return self._get_min()[1]

    @property
    def y_max(self) -> float:
        return self._get_max()[1]

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self.set_rotation(value)

    @property
    def area(self) -> float:
        return self.polygon.area

    @property
    def millable(self) -> bool:
        return self._millable

    @millable.setter
    def millable(self, millable: bool) -> None:
        """Defines wether the shape's interior should be milled or not."""
        if not isinstance(millable, bool):
            raise TypeError(f"Expected 'bool', got '{type(millable)}'.")
        self._millable = millable

    # endregion Properties


# endregion Shape Base Class


# region Combined Shape
class CopyKwargs(TypedDict, total=False):
    x: float
    y: float
    rotation: float


class CombinedShape(Shape):
    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()

    # Instance variables
    _shapes: List[Shape]

    # endregion Class Body

    # region Dev Methods

    def _get_polygon(self) -> Polygon:

        millable = []
        non_millable = []
        for shape in self._shapes:
            if shape._millable:
                millable.append(shape.polygon)
            else:
                non_millable.append(shape.polygon)

        total_millable = unary_union(millable)
        total_non_millable = unary_union(non_millable)

        polygon = total_millable.difference(total_non_millable)

        polygon = self._apply_translation(polygon)
        polygon = self._apply_rotation(polygon)
        return polygon

    # endregion Dev Methods

    # region User Methods

    def rotate(self, rot_angle: float, rot_point: Tuple[float, float] | Shape = None) -> rotate:
        for shape in self._shapes:
            shape.rotate(shape.rotation - self._rotation + rot_angle, rot_point=self)
        super().rotate(rot_angle, rot_point)

    def set_rotation(self, rot_angle: float) -> None:
        for shape in self._shapes:
            rotate_by = shape.rotation - self._rotation + rot_angle
            shape.rotate(rotate_by, rot_point=self)

    def set_position(self, x: float | Shape = None, y: float | Shape = None) -> None:
        for shape in self._shapes:
            shape.x = shape.x - self._x + x if x is not None else shape.x
            shape.y = shape.y - self._y + y if y is not None else shape.y
        super().set_position(x, y)

    def copy(self, **kwargs: Unpack[CopyKwargs]) -> CombinedShape:
        new_shapes = [shape.copy(add_to_pattern=False) for shape in self._shapes]
        new_combined = CombinedShape(self._pattern)
        new_combined._shapes = new_shapes
        for k, v in kwargs.items():
            setattr(new_combined, k, v)
        new_combined._add_to_pattern()
        return new_combined

    # endregion User Methods

    # region Properties

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        for shape in self._shapes:
            shape.x = shape.x - self._x + x
        self._x = x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        for shape in self._shapes:
            shape.y = shape.y - self._y + y
        self._y = y

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

    @property
    def x_span(self) -> float:
        return self.x_max - self.x_min

    @property
    def y_span(self) -> float:
        return self.y_max - self.y_min

    # endregion Properties

# endregion Combined Shape

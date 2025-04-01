from __future__ import annotations

# Std lib
from typing import TypedDict, Unpack, Tuple

# 3rd party lib
from shapely import Polygon, Point, MultiPolygon, box, unary_union
from shapely.affinity import scale

# Loacal lib
from .shape import Shape


class RectangleKwargs(TypedDict, total=False):
    x: float
    y: float
    x_span: float
    y_span: float
    corner_radius: float
    rotation: float
    millable: bool


class Rectangle(Shape):

    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"x_span": 100, "y_span": 100, "corner_radius": 0})

    # Instance variables
    _x_span: float
    _y_span: float
    _corner_radius: float

    __slots__ = ["_x_span", "_y_span", "_corner_radius"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, **kwargs: Unpack[RectangleKwargs]) -> None:
        super().__init__(**kwargs)
        if self._corner_radius * 2 > self._x_span or self._corner_radius * 2 > self._y_span:
            raise ValueError(f"Corner radius cannot be greater than x/y-span.")

    def __repr__(self) -> str:
        output = (
            f"Shape: Rectangle\n"
            f"\tx: {self._x}\n"
            f"\ty: {self._y}\n"
            f"\tx span: {self._x_span}\n"
            f"\ty span: {self._y_span}\n"
            f"\tcorner radius: {self._corner_radius}\n"
            f"\trotation (deg): {self._rotation}\n"
        )
        return output

    def _get_polygon(self) -> Polygon:

        polygon = scale(box(-0.5, -0.5, 0.5, 0.5), self._x_span, self._y_span)
        if self._corner_radius != 0:
            x, y = polygon.exterior.coords.xy
            radius = self._corner_radius
            points = [Point(min(x) + radius, max(y) - radius), Point(min(x) + radius, min(y) + radius),
                      Point(max(x) - radius, max(y) - radius), Point((max(x) - radius), min(y) + radius)]
            circles: MultiPolygon = unary_union([point.buffer(radius, resolution=100) for point in points])
            polygon = circles.convex_hull
        polygon = self._apply_translation(polygon)
        return self._apply_rotation(polygon)

    def _get_max(self) -> Tuple[float, float]:

        if self._rotation in [0, 180]:
            return self._x + self._x_span/2, self._y + self._y_span/2
        elif self._rotation in [90, 270]:
            return self._x + self._y_span/2, self._y + self._x_span/2
        else:
            return super()._get_max()

    def _get_min(self) -> Tuple[float, float]:

        if self._rotation in [0, 180]:
            return self._x - self._x_span/2, self._y - self._y_span/2
        elif self._rotation in [90, 270]:
            return self._x - self._y_span/2, self._y - self._x_span/2
        else:
            return super()._get_min()

    # endregion Dev Methods

    # region User Methods

    def copy(self, **kwargs) -> Rectangle:
        return super().copy(**kwargs)

    # endregion User Methods

    # region Properties

    @property
    def x_span(self) -> float:
        return self.x_span

    @x_span.setter
    def x_span(self, value: float):
        self.x_span = float(value)

    @property
    def y_span(self) -> float:
        return self._y_span

    @y_span.setter
    def y_span(self, value: float):
        self.y_span = float(value)

    @property
    def corner_radius(self) -> float:
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, radius: float) -> None:
        if radius * 2 > self._x_span or radius * 2 > self._y_span:
            raise  ValueError(f"Corner corner radius * 2 cannot be greater than the spans.")
        self._corner_radius = radius

    # endregion Properties

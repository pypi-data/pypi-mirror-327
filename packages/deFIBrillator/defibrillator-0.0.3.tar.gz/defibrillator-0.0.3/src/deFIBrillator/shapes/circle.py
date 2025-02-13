from __future__ import annotations

# Std lib
from typing import TypedDict, Unpack, Tuple

# 3rd party lib
from shapely import Polygon, Point
from shapely.affinity import scale

# Loacal lib
from .shape import Shape


class CircleKwargs(TypedDict, total=False):
    x: float
    y: float
    radius: float
    radius_2: float
    rotation: float
    millable: bool


class Circle(Shape):

    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"radius": 50, "radius_2": None})

    # Instance variables
    _radius: float
    _radius_2: float

    __slots__ = ["_radius", "_radius_2"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, **kwargs: Unpack[CircleKwargs]) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        radius_2 = f"\tradius 2: {self._radius_2}\n" if self._radius_2 is not None else ""
        output = (
            f"Shape: Circle\n"
            f"\tx: {self._x}\n"
            f"\ty: {self._y}\n"
            f"\tradius: {self._radius}\n"
            f"{radius_2}"
            f"\trotation (deg): {self._rotation}\n"
        )
        return output

    def _get_polygon(self) -> Polygon:

        radius_2 = self._radius if self._radius_2 is None else self._radius_2
        polygon = Point((0, 0)).buffer(1, resolution=100)
        polygon = self._apply_translation(polygon)
        polygon = scale(polygon, self._radius, radius_2)
        return self._apply_rotation(polygon)

    def _get_max(self) -> Tuple[float, float]:
        # Fetch the secondary radius
        if self._radius_2 is None:
            radius_2 = self._radius
        else:
            radius_2 = self._radius_2

        if self._rotation in [0, 180]:
            return self._x + self.radius, self._y + radius_2
        elif self._rotation in [90, 270]:
            return self._x + radius_2, self._y + self._radius
        else:
            return super()._get_max()

    def _get_min(self) -> Tuple[float, float]:
        # Fetch the secondary radius
        if self._radius_2 is None:
            radius_2 = self._radius
        else:
            radius_2 = self._radius_2

        if self._rotation in [0, 180]:
            return self._x - self.radius, self._y - radius_2
        elif self._rotation in [90, 270]:
            return self._x - radius_2, self._y - self._radius
        else:
            return super()._get_min()

    # endregion Dev Methods

    # region User Methods

    def copy(self, **kwargs) -> Circle:
        return super().copy(**kwargs)

    # endregion User Methods

    # region Properties

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        self._radius = float(value)

    @property
    def radius_2(self) -> float:
        if self._radius_2 is None:
            return self._radius
        return self._radius_2

    @radius_2.setter
    def radius_2(self, value: float):
        self._radius_2 = float(value)

    # endregion Properties
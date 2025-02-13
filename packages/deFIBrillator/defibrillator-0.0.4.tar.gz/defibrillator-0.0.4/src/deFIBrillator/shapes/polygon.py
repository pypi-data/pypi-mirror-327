from __future__ import annotations

# Std lib
from typing import TypedDict, Unpack, Tuple, Iterable, List

# 3rd party lib
from shapely import Polygon
from shapely.affinity import translate

# Local lib
from .shape import Shape


class PolyKwargs(TypedDict, total=False):
    millable: bool
    x: float
    y: float
    vertices: Iterable[Tuple[float, float]]
    rotation: float


class Poly(Shape):

    # region Class Body

    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"vertices": [(3.061616997868383e-15, 50.0), (-43.30127018922193, -25.000000000000007),
                                           (43.30127018922192, -25.00000000000002)]})

    _vertices: List[Tuple[float, float]]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, **kwargs: Unpack[PolyKwargs]):
        super().__init__(**kwargs)

    def _get_polygon(self, **kwargs: Unpack[PolyKwargs]) -> Polygon:

        polygon = Polygon(self._vertices)
        polygon = translate(polygon, -polygon.centroid.x, -polygon.centroid.y)

        # Apply translation and rotation if needed
        polygon = self._apply_translation(polygon)
        polygon = self._apply_rotation(polygon)

        # Initialize the shape with final polygon
        return polygon

    # endregion Dev Methods

    # region User Methods

    def copy(self, **kwargs: Unpack[PolyKwargs]) -> Poly:
        return super().copy(**kwargs)

    # endregion User Methods

    # region Properties

    @property
    def vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the polygon's vertices."""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: List[Tuple[float, float]]) -> None:
        """Sets the list of vertices for the polygon."""
        self._vertices = vertices

    # endregion Properties

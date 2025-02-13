from __future__ import annotations

# Std lib
from typing import Unpack, TypedDict

# 3rd party lib
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from shapely import Polygon, MultiPolygon, unary_union

# Local lib
from .shape import Shape


class TextKwargs(TypedDict, total=False):
    x: float
    y: float
    font_size: int
    millable: bool


class Text(Shape):

    # region Class Body

    # Class variables
    _default_geometry = Shape._default_geometry.copy()
    _default_geometry.update({"fontsize": 1000})

    # Instance variables
    _fontsize: int
    _text: str

    __slots__ = ["_fontsize", "_text"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, text: str, **kwargs: Unpack[TextKwargs]) -> None:
        super().__init__(**kwargs)
        self._text = text

    def _get_polygon(self) -> MultiPolygon:
        """
        Converts a given text string into a Shapely MultiPolygon.

        Parameters:
        text (str): The text string to convert.
        font_path (str, optional): Path to a .ttf font file. Defaults to the system's default font.
        size (int, optional): Font size. Defaults to 1.

        Returns:
        MultiPolygon: The resulting MultiPolygon geometry of the text.
        """
        # Set up font properties
        font_prop = FontProperties()

        # Create the text path at origin (0, 0)
        path = TextPath(self._get_absolute_position(), self._text, size=self._fontsize * (1 / 0.725), prop=font_prop)

        # Extract polygons from the path
        polygons = []
        for vertices in path.to_polygons():
            if len(vertices) >= 3:  # Ensure polygon has at least 3 points
                polygons.append(Polygon(vertices))

        # Union polygons to handle overlaps and holes
        if not polygons:
            return MultiPolygon()
        union = unary_union(polygons)

        # Return as a MultiPolygon
        if union.geom_type == 'Polygon':
            return MultiPolygon([union])
        return union

    # endregion Dev Methods

    # region User Methods

    def copy(self, **kwargs) -> Text:
        return super().copy(**kwargs)

    # endregion User Methods

    # region Properties

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = str(text)

    @property
    def font_size(self) -> int:
        return self._fontsize

    @font_size.setter
    def font_size(self, value: int):
        self._fontsize = int(value)

    # endregion Properties

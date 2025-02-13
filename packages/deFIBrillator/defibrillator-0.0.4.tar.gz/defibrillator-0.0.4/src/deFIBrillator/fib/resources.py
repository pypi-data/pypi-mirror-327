from typing import Tuple, Literal

MagnificationHint = Tuple[int, float, float]
ScanStyles = Literal["contour inwards", "contour outwards", "serpentine single horizontal",
                     "serpentine single vertical", "serpentine double horizontal", "serpentine double vertical",
                     "raster left-right bottom-top", "raster right-left, bottom top", "raster left-right top-bottom",
                     "raster right-left top-bottom"]
Voltages = Literal["500V", "1kV", "2kV", "5kV", "8kV", "16kV", "30kV"]
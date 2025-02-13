# Std lib
from abc import ABC, abstractmethod
from typing import ClassVar, List, Type

# 3rd party lib
import numpy as np
from matplotlib import pyplot as plt

# Local lib
from .resources import MagnificationHint
from ..beams import BeamType
from ..pattern import Pattern
from ..resources import LENGTHUNITS, length_units


class FIB(ABC):

    # region Class Body

    # Class variables
    _fov_1000x: ClassVar[float]
    _fov_pixels: ClassVar[int]
    _default_beam: Type[BeamType]

    # Instance variables
    _magnification: int
    _beam: BeamType
    _patterns: List[Pattern]

    # endregion Class Body

    # region Dev Methods

    def __init__(self, magnification: int = None) -> None:
        if magnification is None:
            self._magnification = 1000  # Default magnification is 1000x
        else:
            self.set_magnification(magnification)
        self._patterns = []
        self._beam = self._default_beam()

    # endregion Dev Methods

    # region User Methods

    def set_magnification(self, magnification: int) -> None:
        """Sets the magnification of the FIB instance."""
        self._magnification = magnification

    def get_fov(self, units: LENGTHUNITS = "nm") -> float:
        """Gets the field of view of the FIB monitor in nanometers based on the current magnification."""
        return length_units(self._fov_1000x, "nm", units) * (1000 / self._magnification)

    def set_fov(self, fov: float, units: LENGTHUNITS = "nm"):
        """Sets the magnification that provides the field of view closest to the one provided. Returns a tuple
        with the magnification, and the actual field of view in the same units as provided."""
        closest_mag = int(np.round((1000 / length_units(fov, units, "nm")) * self._fov_1000x))
        fov = (1000 / closest_mag) * self._fov_1000x
        self._magnification = closest_mag
        return closest_mag, length_units(fov, "nm", units)

    def get_pixelsize(self, units: LENGTHUNITS = "nm") -> float:
        """Gets the size of each pixel in the field of view in nanometers [nm]."""
        return self.get_fov(units) / self._fov_pixels

    def new_pattern(self, x: float = 0, y: float = 0) -> Pattern:
        pattern = Pattern(self, x, y)
        self._patterns.append(pattern)
        return pattern

    def set_beam(self, beam: Type[BeamType]) -> None:
        self._beam = beam()

    def get_magnification_hint(self, desired_pixelsize: float, units: LENGTHUNITS = "nm") -> MagnificationHint:
        closest_mag = int(np.round((1000 * self._fov_1000x
                                    / (length_units(desired_pixelsize, units, "nm") * self._fov_pixels))))
        effective_pixelsize = (1000 * self._fov_1000x) / (closest_mag * self._fov_pixels)
        fov = (1000 / closest_mag) * self._fov_1000x
        return closest_mag, effective_pixelsize, length_units(fov, "nm", units)

    def get_magnification_stats(self, magnification: int, units: LENGTHUNITS = "nm") -> MagnificationHint:
        effective_pixelsize = (1000 * self._fov_1000x) / (magnification * self._fov_pixels)
        fov = (1000 / magnification) * self._fov_1000x
        return magnification, effective_pixelsize, length_units(fov, "nm", units)

    def draw_patterns(self) -> None:
        ax = None
        for pattern in self._patterns:
            ax = pattern._get_pattern_ax(ax)
        ax.relim()
        ax.autoscale_view()
        ax.set_aspect('equal')
        plt.show()

    # endregion User Methods

    # region Properties

    @property
    def beam(self) -> BeamType:
        return self._beam

    @property
    def magnification(self) -> int:
        """Gets the magnification of the FIBG2 instance."""
        return self._magnification

    @magnification.setter
    def magnification(self, magnification: int) -> None:
        """Sets the magnification of the FIBG2 instance."""
        if not isinstance(magnification, int):
            raise TypeError(f"Got '{type(magnification)}', expected 'type(int)'.")
        elif magnification < 150:
            raise ValueError(f"Magnification '{magnification}' is lower than the FIB's lowest magnification of 150x.")
        else:
            self._magnification = magnification

    # endregion Properties

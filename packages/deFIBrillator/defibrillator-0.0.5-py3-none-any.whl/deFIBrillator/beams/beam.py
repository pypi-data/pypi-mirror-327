# Std lib
from abc import ABC
from typing import TypeVar

# 3rd party lib
import numpy as np

# Local lib
from ..resources import (length_units, current_units, voltage_units, LENGTHUNITS, CURRENTUNITS, VOLTAGEUNITS,
                         TIMEUNITS, time_units as t_u, DOSEUNITS, dose_units as d_u)


BeamType = TypeVar("BeamType", bound="Beam")


class Beam(ABC):

    # region Class Body

    _beam_diameter: float
    _current: float
    _voltage: float

    # endregion Class Body

    # region Dev Methods

    def __repr__(self) -> str:
        if self.get_current() < 100:
            current = f"{self.get_current("pa")} pA"
        else:
            current = f"{self.get_current("na")} nA"
        return (f"Ion Beam:\n"
                f"\tAcceleration voltage: {self.get_voltage("kv")} V\n"
                f"\tCurrent: {current}\n"
                f"\tBeam Diameter: {self.get_diameter("nm")} nm\n"
                f"\tBeam Radius: {self.get_radius("nm")} nm\n"
                f"\tBeam Area: {self.get_area("nm")} nm²")

    # endregion Dev Methods

    # region User Methods

    def get_dose(self, dwell_time: float, time_units: TIMEUNITS = "us", dose_units: DOSEUNITS = "nc") -> float:
        """Calculates and returns the dose in the specified dose units provided to a beam spot in a
        given dwell time [specified time units]."""
        return d_u((self._current * t_u(dwell_time, time_units, "s")) / ((self.get_radius("um")) ** 2),
                   "c", dose_units)

    def get_current(self, units: CURRENTUNITS = "na") -> float:
        """Return the beam current in the provided current units."""
        return current_units(self._current, "a", units)

    def get_area(self, units: LENGTHUNITS = "nm") -> float:
        """Return the beam area in the desired units squared."""
        return np.pi * np.pow(self.get_radius(units), 2)

    def get_diameter(self, units: LENGTHUNITS = "nm") -> float:
        """Returns the beam diameter in the desired length units.."""
        return length_units(self._beam_diameter, "m", units)

    def get_radius(self, units: LENGTHUNITS = "nm") -> float:
        """Returns the beam radius in the desired length units."""
        return self.get_diameter(units) / 2

    def get_voltage(self, units: VOLTAGEUNITS) -> float:
        """Returns the acceleration voltage of the beam in the desired voltage units."""
        return voltage_units(self._voltage, "v", units)

    # endregion User Methods


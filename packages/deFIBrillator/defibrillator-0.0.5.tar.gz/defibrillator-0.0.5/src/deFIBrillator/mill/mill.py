from ..resources import time_units, TIMEUNITS, LENGTHUNITS, length_units


class Mill:

    # region Class Body

    _overlap: float
    _dwell_time: float
    _depth: float

    __slots__ = ["_overlap", "_dwell_time", "_depth"]

    # endregion Class Body

    # region Dev Methods

    def __init__(self) -> None:
        self.set_overlap(0.5)
        self.set_dwell_time(1, "us")
        self.set_mill_depth(0.5, "um")

    # endregion Dev Methods

    # region User Methods

    def get_mill_depth(self, units: LENGTHUNITS = "um") -> float:
        """Returns the milling depth in the desired units."""
        return length_units(self._depth, "m", units)

    def set_mill_depth(self, depth: float, units: LENGTHUNITS = "um"):
        """Sets the milling depth in the provided units."""
        self._depth = length_units(depth, units, "m")

    def get_overlap(self) -> float:
        """Returns the fraction of overlap between adjacent beam points in nanometers [nm]."""
        return self._overlap

    def set_overlap(self, overlap: float) -> None:
        """Sets the fraction of overlap between adjacent beam spots in nanometers [nm]."""
        if overlap >= 1:
            raise ValueError(f"The overlap fraction must be below 1, corresponding to 100%, not '{overlap}'.")
        self._overlap = overlap

    def get_dwell_time(self, units: TIMEUNITS = "us") -> float:
        """Returns the base dwell time pr. point in the desired time units."""
        return time_units(self._dwell_time, "s", units)

    def set_dwell_time(self, dwell_time: float, units: TIMEUNITS = "us") -> None:
        """Sets the base dwell time pr. point in the desired units."""
        dwell = time_units(dwell_time, units, "s")
        if dwell < 25e-9:
            raise ValueError(f"The minimum dwell time is 25 nanoseconds. Got '{dwell_time} {units}'.")
        self._dwell_time = dwell

    # endregion User Methods

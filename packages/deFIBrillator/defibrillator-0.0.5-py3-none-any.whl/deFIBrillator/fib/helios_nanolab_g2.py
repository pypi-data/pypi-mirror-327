# Local lib
import sys

from .fib import FIB
from ..beams import IonBeams


class FIBG2(FIB):

    # region Class Body

    # Class variables
    _fov_1000x = 128_000
    _fov_pixels = 65536
    _default_beam = IonBeams.Acceleration30kV.pA48

    # Instance variables
    Beams: IonBeams

    # endregion Class Body

    # region Dev Methods

    def __init__(self, magnification: int = None) -> None:
        super().__init__(magnification)
        self.Beams = IonBeams()

    def __repr__(self) -> str:
        return (f"FEI Helios Nanolab Dualbeam G2:\n"
                f"\tMagnification: {self._magnification}\n"
                f"\tField of view: {self.get_fov("um")} um\n"
                f"\tPixelsize: {self.get_pixelsize("nm")} nm\n"
                f"{self.beam}")

    # endregion Dev Methods

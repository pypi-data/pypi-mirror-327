from typing import Literal

# region Constants and Literals

LENGTHUNITS = Literal["m", "cm", "mm", "um", "nm"]
CURRENTUNITS = Literal["a", "ma", "ua", "na", "pa"]
DOSEUNITS = Literal["c", "mc", "uc", "nc", "pc"]
VOLTAGEUNITS = Literal["v", "kv"]
TIMEUNITS = Literal["s", "ms", "us", "ns"]
DECIMALS = 15
CONVERSIONS = {
    "m": 1,
    "cm": 100,
    "mm": 1000,
    "um": 1e6,
    "nm": 1e9,
    "a": 1,
    "ma": 1000,
    "ua": 1e6,
    "na": 1e9,
    "pa": 1e12,
    "c": 1,
    "mc": 1000,
    "uc": 1e6,
    "nc": 1e9,
    "pc": 1e12,
    "v": 1,
    "kv": 1000,
    "s": 1,
    "ms": 1000,
    "us": 1e6,
    "ns": 1e9
}


# endregion Constants and Literals

# region Functions

def convert_units(value: float, from_unit: str, to_unit: str, power: int = 1) -> float:
    from_factor = CONVERSIONS[from_unit]
    to_factor = CONVERSIONS[to_unit]
    converted_value = value * (to_factor / from_factor) ** power
    return round(converted_value, DECIMALS)


def dose_units(value: float, original: DOSEUNITS, to: DOSEUNITS, power: int = 1) -> float:
    return convert_units(value, from_unit=original, to_unit=to, power=power)


def length_units(value: float, original: LENGTHUNITS, to: LENGTHUNITS, power: int = 1) -> float:
    return convert_units(value, from_unit=original, to_unit=to, power=power)


def current_units(value: float, original: CURRENTUNITS, to: CURRENTUNITS, power: int = 1) -> float:
    return convert_units(value, from_unit=original, to_unit=to, power=power)


def voltage_units(value: float, original: VOLTAGEUNITS, to: VOLTAGEUNITS) -> float:
    return convert_units(value, from_unit=original, to_unit=to)


def time_units(value: float, original: TIMEUNITS, to: TIMEUNITS) -> float:
    return convert_units(value, original, to)

# endregion Functions

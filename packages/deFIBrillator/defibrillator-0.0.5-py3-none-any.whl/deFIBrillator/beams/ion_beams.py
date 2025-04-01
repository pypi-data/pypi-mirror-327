# Local lib
from .beam import Beam


class IonBeams:

    # region 500V
    class Acceleration500V:
        class pA1_5(Beam):
            _beam_diameter: float = 2.52e-07
            _current: float = 1.5e-12
            _voltage: float = 500

        class pA6(Beam):
            _beam_diameter: float = 4.98e-07
            _current: float = 6e-12
            _voltage: float = 500

        class pA15(Beam):
            _beam_diameter: float = 7.79e-07
            _current: float = 1.5e-11
            _voltage: float = 500

        class pA24(Beam):
            _beam_diameter: float = 9.96e-07
            _current: float = 2.4e-11
            _voltage: float = 500

        class pA42(Beam):
            _beam_diameter: float = 1.311e-06
            _current: float = 4.2e-11
            _voltage: float = 500

        class nA0_11(Beam):
            _beam_diameter: float = 2.136e-06
            _current: float = 1.1e-10
            _voltage: float = 500

        class nA0_18(Beam):
            _beam_diameter: float = 2.771e-06
            _current: float = 1.8e-10
            _voltage: float = 500

        class nA0_33(Beam):
            _beam_diameter: float = 3.96e-06
            _current: float = 3.3e-10
            _voltage: float = 500

        class nA0_92(Beam):
            _beam_diameter: float = 9.27e-06
            _current: float = 9.2e-10
            _voltage: float = 500

        class nA2(Beam):
            _beam_diameter: float = 2.442e-05
            _current: float = 2e-09
            _voltage: float = 500

        class nA2_8(Beam):
            _beam_diameter: float = 3.8445e-05
            _current: float = 2.8e-09
            _voltage: float = 500

        class nA21(Beam):
            _beam_diameter: float = 0.00075
            _current: float = 2.1e-08
            _voltage: float = 500

    # endregion 500V

    # region 1kV
    class Acceleration1kV:
        class pA0_7(Beam):
            _beam_diameter: float = 8e-08
            _current: float = 7e-13
            _voltage: float = 1

        class pA2_3(Beam):
            _beam_diameter: float = 1.1e-07
            _current: float = 2.3e-12
            _voltage: float = 1

        class pA5_3(Beam):
            _beam_diameter: float = 1.43e-07
            _current: float = 5.3e-12
            _voltage: float = 1

        class pA8_6(Beam):
            _beam_diameter: float = 1.68e-07
            _current: float = 8.6e-12
            _voltage: float = 1

        class pA14(Beam):
            _beam_diameter: float = 2e-07
            _current: float = 1.4e-11
            _voltage: float = 1

        class pA36(Beam):
            _beam_diameter: float = 2.88e-07
            _current: float = 3.6e-11
            _voltage: float = 1

        class pA59(Beam):
            _beam_diameter: float = 3.53e-07
            _current: float = 5.9e-11
            _voltage: float = 1

        class nA0_11(Beam):
            _beam_diameter: float = 4.59e-07
            _current: float = 1.1e-10
            _voltage: float = 1

        class nA0_3(Beam):
            _beam_diameter: float = 7.49e-07
            _current: float = 3e-10
            _voltage: float = 1

        class nA0_66(Beam):
            _beam_diameter: float = 1.092e-06
            _current: float = 6.6e-10
            _voltage: float = 1

        class nA0_92(Beam):
            _beam_diameter: float = 1.284e-06
            _current: float = 9.2e-10
            _voltage: float = 1

        class nA6_9(Beam):
            _beam_diameter: float = 3.927e-06
            _current: float = 6.9e-09
            _voltage: float = 1

    # endregion 1kV

    # region 2kV
    class Acceleration2kV:
        class pA0_3(Beam):
            _beam_diameter: float = 3.9e-08
            _current: float = 3e-13
            _voltage: float = 2

        class pA1_3(Beam):
            _beam_diameter: float = 5.1e-08
            _current: float = 1.3e-12
            _voltage: float = 2

        class pA3_2(Beam):
            _beam_diameter: float = 6.5e-08
            _current: float = 3.2e-12
            _voltage: float = 2

        class pA5_5(Beam):
            _beam_diameter: float = 7.7e-08
            _current: float = 5.5e-12
            _voltage: float = 2

        class pA10(Beam):
            _beam_diameter: float = 9.2e-08
            _current: float = 1e-11
            _voltage: float = 2

        class pA28(Beam):
            _beam_diameter: float = 1.26e-07
            _current: float = 2.8e-11
            _voltage: float = 2

        class pA46(Beam):
            _beam_diameter: float = 1.5e-07
            _current: float = 4.6e-11
            _voltage: float = 2

        class pA89(Beam):
            _beam_diameter: float = 1.95e-07
            _current: float = 8.9e-11
            _voltage: float = 2

        class nA0_25(Beam):
            _beam_diameter: float = 2.99e-07
            _current: float = 2.5e-10
            _voltage: float = 2

        class nA0_56(Beam):
            _beam_diameter: float = 4.32e-07
            _current: float = 5.6e-10
            _voltage: float = 2

        class nA0_77(Beam):
            _beam_diameter: float = 5.07e-07
            _current: float = 7.7e-10
            _voltage: float = 2

        class nA6_7(Beam):
            _beam_diameter: float = 1.935e-06
            _current: float = 6.7e-09
            _voltage: float = 2

    # endregion 2kV

    # region 5kV
    class Acceleration5kV:
        class pA0_4(Beam):
            _beam_diameter: float = 2e-08
            _current: float = 4e-13
            _voltage: float = 5

        class pA1_6(Beam):
            _beam_diameter: float = 2.7e-08
            _current: float = 1.6e-12
            _voltage: float = 5

        class pA4_4(Beam):
            _beam_diameter: float = 3.5e-08
            _current: float = 4.4e-12
            _voltage: float = 5

        class pA8(Beam):
            _beam_diameter: float = 4.1e-08
            _current: float = 8e-12
            _voltage: float = 5

        class pA16(Beam):
            _beam_diameter: float = 4.8e-08
            _current: float = 1.6e-11
            _voltage: float = 5

        class pA47(Beam):
            _beam_diameter: float = 6.7e-08
            _current: float = 4.7e-11
            _voltage: float = 5

        class pA81(Beam):
            _beam_diameter: float = 8e-08
            _current: float = 8.1e-11
            _voltage: float = 5

        class nA0_15(Beam):
            _beam_diameter: float = 9.6e-08
            _current: float = 1.5e-10
            _voltage: float = 5

        class nA0_45(Beam):
            _beam_diameter: float = 1.43e-07
            _current: float = 4.5e-10
            _voltage: float = 5

        class nA1(Beam):
            _beam_diameter: float = 2.07e-07
            _current: float = 1e-09
            _voltage: float = 5

        class nA1_5(Beam):
            _beam_diameter: float = 2.51e-07
            _current: float = 1.5e-09
            _voltage: float = 5

        class nA12(Beam):
            _beam_diameter: float = 1.4e-06
            _current: float = 1.2e-08
            _voltage: float = 5

    # endregion 5kV

    # region 8kV
    class Acceleration8kV:
        class pA0_5(Beam):
            _beam_diameter: float = 1.2e-08
            _current: float = 5e-13
            _voltage: float = 8

        class pA1_9(Beam):
            _beam_diameter: float = 1.6e-08
            _current: float = 1.9e-12
            _voltage: float = 8

        class pA5_7(Beam):
            _beam_diameter: float = 2.2e-08
            _current: float = 5.7e-12
            _voltage: float = 8

        class pA11(Beam):
            _beam_diameter: float = 2.6e-08
            _current: float = 1.1e-11
            _voltage: float = 8

        class pA21(Beam):
            _beam_diameter: float = 3e-08
            _current: float = 2.1e-11
            _voltage: float = 8

        class pA62(Beam):
            _beam_diameter: float = 4.1e-08
            _current: float = 6.2e-11
            _voltage: float = 8

        class nA0_11(Beam):
            _beam_diameter: float = 5e-08
            _current: float = 1.1e-10
            _voltage: float = 8

        class nA0_22(Beam):
            _beam_diameter: float = 6.3e-08
            _current: float = 2.2e-10
            _voltage: float = 8

        class nA0_66(Beam):
            _beam_diameter: float = 9e-08
            _current: float = 6.6e-10
            _voltage: float = 8

        class nA1_6(Beam):
            _beam_diameter: float = 1.33e-07
            _current: float = 1.6e-09
            _voltage: float = 8

        class nA2_2(Beam):
            _beam_diameter: float = 1.59e-07
            _current: float = 2.2e-09
            _voltage: float = 8

        class nA19(Beam):
            _beam_diameter: float = 1.056e-06
            _current: float = 1.9e-08
            _voltage: float = 8

    # endregion 8kV

    # region 16kV
    class Acceleration16kV:
        class pA0_6(Beam):
            _beam_diameter: float = 1.2e-08
            _current: float = 6e-13
            _voltage: float = 16

        class pA3_4(Beam):
            _beam_diameter: float = 1.9e-08
            _current: float = 3.4e-12
            _voltage: float = 16

        class pA11(Beam):
            _beam_diameter: float = 2.5e-08
            _current: float = 1.1e-11
            _voltage: float = 16

        class pA21(Beam):
            _beam_diameter: float = 2.9e-08
            _current: float = 2.1e-11
            _voltage: float = 16

        class pA45(Beam):
            _beam_diameter: float = 3.4e-08
            _current: float = 4.5e-11
            _voltage: float = 16

        class nA0_13(Beam):
            _beam_diameter: float = 4.5e-08
            _current: float = 1.3e-10
            _voltage: float = 16

        class nA0_24(Beam):
            _beam_diameter: float = 5.4e-08
            _current: float = 2.4e-10
            _voltage: float = 16

        class nA0_47(Beam):
            _beam_diameter: float = 6.6e-08
            _current: float = 4.7e-10
            _voltage: float = 16

        class nA1_4(Beam):
            _beam_diameter: float = 9.3e-08
            _current: float = 1.4e-09
            _voltage: float = 16

        class nA3_3(Beam):
            _beam_diameter: float = 1.3e-07
            _current: float = 3.3e-09
            _voltage: float = 16

        class nA4_7(Beam):
            _beam_diameter: float = 1.55e-07
            _current: float = 4.7e-09
            _voltage: float = 16

        class nA21(Beam):
            _beam_diameter: float = 5.2e-07
            _current: float = 2.1e-08
            _voltage: float = 16

    # endregion 16kV

    # region 30kV
    class Acceleration30kV:
        class pA1_5(Beam):
            _beam_diameter: float = 7e-09
            _current: float = 1.5e-12
            _voltage: float = 30

        class pA9_7(Beam):
            _beam_diameter: float = 1.3e-08
            _current: float = 9.7e-12
            _voltage: float = 30

        class pA28(Beam):
            _beam_diameter: float = 1.7e-08
            _current: float = 2.8e-11
            _voltage: float = 30

        class pA48(Beam):
            _beam_diameter: float = 1.9e-08
            _current: float = 4.8e-11
            _voltage: float = 30

        class pA93(Beam):
            _beam_diameter: float = 2.4e-08
            _current: float = 9.3e-11
            _voltage: float = 30

        class nA0_28(Beam):
            _beam_diameter: float = 3.1e-08
            _current: float = 2.8e-10
            _voltage: float = 30

        class nA0_46(Beam):
            _beam_diameter: float = 3.5e-08
            _current: float = 4.6e-10
            _voltage: float = 30

        class nA0_92(Beam):
            _beam_diameter: float = 4.4e-08
            _current: float = 9.2e-10
            _voltage: float = 30

        class nA2_8(Beam):
            _beam_diameter: float = 6.6e-08
            _current: float = 2.8e-09
            _voltage: float = 30

        class nA6_5(Beam):
            _beam_diameter: float = 1.02e-07
            _current: float = 6.5e-09
            _voltage: float = 30

        class nA9_3(Beam):
            _beam_diameter: float = 1.29e-07
            _current: float = 9.3e-09
            _voltage: float = 30

        class nA21(Beam):
            _beam_diameter: float = 2.74e-07
            _current: float = 2.1e-08
            _voltage: float = 30
    # endregion 30kV

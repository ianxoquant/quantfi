import numpy as np
import unittest

"""Hull White cap and swaption calculators"""
"""After Brigo/Mercurio Second Edition pp71-77"""


def AtT(r, a, v, t, T):
    pass


def BtT(a, t, T):
    if a == 0.0:  # TODO should be an eps test?
        return(T-t)
    else:
        # TODO check if this is correct for negative reversion
        return((1.0/a*(1.0 - np.exp(-a*(T-t)))))


def PtT(r, a, v, t, T):
    pass


def VtT(a, v, t, T):
    """Price volatility of a zero coupon bond"""
    """Note that this is a term vol not an annualized vol"""
    """ here t is expiration or S in Brigo notation and T is Maturity"""
    return(v * BtT(a, t, T) * np.sqrt(0.5*BtT(a, 0.0, 2*t)))


def VtTwo(a, v, t, T):
    """Price volatility of a zero coupon bond"""
    """Long hand"""
    return(v/a * (1-np.exp(-a*(T-t))) * np.sqrt((1-np.exp(-2*a*t))/(2*a)))


def ZB():
    pass


def BO():
    pass


class TestHullWhiteFunctions(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_BtT(self):
        self.assertAlmostEqual(BtT(0.0, 5.0, 7.0), 2.0, 9)
        self.assertAlmostEqual(BtT(0.01, 5.0, 7.0),
                               1.9801326693244747, 9)
        self.assertAlmostEqual(BtT(0.015, 5.0, 7.0),
                               1.9702977634327898, 9)

    def test_VtT(self):
        self.assertAlmostEqual(VtT(0.1, 0.02, 3, 5),
                               0.054452531346, 9)
        self.assertAlmostEqual(VtT(0.1, 0.015, 0.25, 1.25),
                               VtTwo(0.1, 0.015, 0.25, 1.25), 9)


if __name__ == '__main__':
    unittest.main()

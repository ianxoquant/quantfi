import numpy as np
import unittest

"""Hull White cap and swaption calculators"""
"""After Brigo/Mercurio Second Edition pp71-77"""


def AtT(a, v, t, T, DFt, DFT, f):

    BtT_value = BtT(a, t, T)
    AtT_value = DFT/DFt * np.exp(BtT_value*f)

    if a == 0.0:  # TODO should be an eps test?
        AtT_value = AtT_value * np.exp(-np.pow(v*BtT_value, 2.0) *
                                       (1.0 - np.exp(-2.0*a*t)))/(4.0*a)
    else:
        AtT_value = AtT_value * np.exp(-np.pow(v*BtT_value, 2.0) * (t/2.0))
    return(AtT_value)


def BtT(a, t, T):
    if a == 0.0:  # TODO should be an eps test?
        return(T-t)
    else:
        # TODO check if this is correct for negative reversion
        return((1.0/a*(1.0 - np.exp(-a*(T-t)))))


def BtTdt(a, t, T, dt):
    return(dt*BtT(a, t, T)/BtT(a, t, T+dt))


def PtTr(a, v, t, T, DFt, DFT, f, r):
    BtT_value = BtT(a, t, T)
    AtT_value = AtT(a, t, T, DFt, DFT, f)

    PtTr_value = AtT_value * np.exp(-BtT_value*r)
    return(PtTr_value)


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

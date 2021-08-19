import numpy as np
import unittest

from scipy.optimize import fsolve

from globals import OptionType
from blackbachelier import black_by_analytic

"""Hull White cap and swaption calculators"""
"""Hull Options, Futures and Other Derivatives 4th Edition p575 -
for the formulae for BtTdt and AtTdt"""
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


def AtTdt(a, v, t, T, dt, DFt, DFT, DFdt):
    """TODO: Add assertion on dt > 0.0"""
    """TODO: Add assertion on a >= 0.0"""
    BtT_value = BtT(a, t, T)
    Btdt_value = BtT(a, t, t + dt)
    AtT_value = DFT/DFt * np.exp(-(BtT_value/Btdt_value)*np.log(DFdt/DFt))
    # print(BtT_value, Btdt_value, AtT_value)

    if a == 0.0:  # TODO should be an eps test?
        AtT_value = AtT_value * np.exp(-(v*v)/(2.0) *
                                       (t)
                                       * BtT_value * (BtT_value - Btdt_value))
    else:
        AtT_value = AtT_value * np.exp(-(v*v)/(4.0*a) *
                                       (1.0 - np.exp(-2.0*a*t))
                                       * BtT_value * (BtT_value - Btdt_value))
    return(AtT_value)


def BtT(a, t, T):
    if a == 0.0:  # TODO should be an eps test?
        return(T-t)
    else:
        # TODO check if this is correct for negative reversion
        return((1.0/a*(1.0 - np.exp(-a*(T-t)))))


def BtTdt(a, t, T, dt):
    return(dt*BtT(a, t, T)/BtT(a, t, t+dt))


def PtTr(a, v, t, T, DFt, DFT, f, r):
    BtT_value = BtT(a, t, T)
    AtT_value = AtT(a, t, T, DFt, DFT, f)

    PtTr_value = AtT_value * np.exp(-BtT_value*r)
    return(PtTr_value)


def PtTdtr(a, v, t, T, dt, DFt, DFT, DFdt, r):
    BtTdr_value = BtTdt(a, t, T, dt)
    AtTdt_value = AtTdt(a, v, t, T, dt, DFt, DFT, DFdt)

    return(AtTdt_value*np.exp(-BtTdr_value*r))


def PtTdtr_array(a, v, t, T, dt, DFt, DFT, DFdt, r):

    if not (len(T) == len(DFT)):
        raise ValueError('PtTdtr_array: length of T must equal length of dfT')

    res = np.empty(0)
    for Tval, DFval in zip(T, DFT):
        BtTdr_value = BtTdt(a, t, Tval, dt)
        AtTdt_value = AtTdt(a, v, t, Tval, dt, DFt, DFval, DFdt)
        res = np.append(res, AtTdt_value*np.exp(-BtTdr_value*r))

    return(res)


def VsT(a, v, s, T):
    """Price volatility of a zero coupon bond"""
    """Note that this is a term vol not an annualized vol"""
    """ here s is expiration and T is Maturity"""
    return(v * BtT(a, s, T) * np.sqrt(0.5*BtT(a, 0.0, 2*s)))


def VsTwo(a, v, s, T):
    """Price volatility of a zero coupon bond"""
    """Long hand, doesn't trap a=0.0"""
    return(v/a * (1-np.exp(-a*(T-s))) * np.sqrt((1-np.exp(-2*a*s))/(2*a)))


def ZBO(option_type, a, v, X, s, T, dfs, dfT):
    """Option on zero coupon bond"""

    # calculate termvol and convert back into annual vol
    volatility = VsT(a, v, s, T)/np.sqrt(s)
    # normal rate process so lognormal zero coupon bond proces
    zb_val = black_by_analytic(option_type, X, dfT/dfs,
                               s, volatility, dfs)

    return(zb_val)


def CBO(option_type, CF, K, s, T, dt, DFs, DFT, DFdt, a, v):
    """Option on par bond using Jamshidians decomposition"""
    """check notional and dfT are the same length"""

    if not isinstance(option_type, OptionType):
        raise TypeError('CBO: option_type must be an instance of OptionType Enum')
    if not (len(CF) == len(T)):
        raise ValueError('CBO: length of cash flows must equal length of T')
    if not (len(T) == len(DFT)):
        raise ValueError('CBO: length of T must equal length of dfT')

    dt = (T[0]-s)

    # guess r_crit as forward at expiration
    r_crit = -np.log(DFdt/DFs)/dt

    r_crit = fsolve(lambda x:
                    K-np.sum(CF*(PtTdtr_array(a, v, s, T, dt, DFs, DFT, DFT[0],  x))), r_crit)

    ZBO_K = PtTdtr_array(a, v, s, T, dt, DFs, DFT, DFT[0], r_crit)
    # TODO catch fsolve error

    res = np.empty(0)
    for Kval, Tval, DFval in zip(ZBO_K, T, DFT):
        res = np.append(res, ZBO(option_type, a, v, Kval, s, Tval, DFs, DFval))

    return(np.sum(res*CF))


class TestHullWhiteFunctions(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def reversion(self):
        return(0.1)

    def volatility(self):
        return(0.015)

    def dfs(self):
        return(np.exp([-0.095*0.25, -0.105*0.75, -0.115*1.25]))

    def test_BtT(self):
        self.assertAlmostEqual(BtT(0.0, 5.0, 7.0), 2.0, 9)
        self.assertAlmostEqual(BtT(0.01, 5.0, 7.0),
                               1.9801326693244747, 9)
        self.assertAlmostEqual(BtT(0.015, 5.0, 7.0),
                               1.9702977634327898, 9)

    def test_AtTdt(self):
        self.assertAlmostEqual(AtTdt(self.reversion(),
                                     self.volatility(),
                                     0.25, 1.25, 0.5,
                                     self.dfs()[0], self.dfs()[2], self.dfs()[1]),
                               0.9873857422763, 9)

    def test_BtTdt(self):
        self.assertAlmostEqual(BtTdt(0.1, 0.25, 1.25, 0.5),
                               0.9756147122503577, 9)

    def test_VsT(self):
        self.assertAlmostEqual(VsT(0.1, 0.02, 3, 5),
                               0.054452531346, 9)
        self.assertAlmostEqual(VsT(0.1, 0.015, 0.25, 1.25),
                               VsTwo(0.1, 0.015, 0.25, 1.25), 9)

    def test_Swaption(self):
        # Hull page 578 example 21.2 - This example only has 2 dp on the options
        # price. TODO: SET UP A SPREADSHEET TO CHECK VALUES TO MORE DECIMALS
        r_star = 0.1067409  # tweaked to match r_crit in the swaption calculator
        self.assertAlmostEqual(6*PtTdtr(self.reversion(),
                                        self.volatility(),
                                        0.25, 0.75, 0.5,
                                        self.dfs()[0], self.dfs()[1], self.dfs()[1],
                                        r_star),
                               5.68814, 4)

        self.assertAlmostEqual(106*PtTdtr(self.reversion(),
                                          self.volatility(),
                                          0.25, 1.25, 0.5,
                                          self.dfs()[0], self.dfs()[2], self.dfs()[1],
                                          r_star),
                               94.31186, 4)

        self.assertAlmostEqual(np.sum(np.array([6, 106]) *
                               PtTdtr_array(self.reversion(),
                                            self.volatility(),
                                            0.25, np.array([0.75, 1.25]), 0.5,
                                            self.dfs()[0], self.dfs()[1:], self.dfs()[1],
                                            r_star)),
                               100.0, 5)

        self.assertAlmostEqual(6*ZBO(OptionType.PUT,
                                     self.reversion(),
                                     self.volatility(),
                                     5.68814/6,
                                     0.25, 0.75,
                                     self.dfs()[0], self.dfs()[1]),
                               0.01, 2)
        self.assertAlmostEqual(106*ZBO(OptionType.PUT,
                                       self.reversion(),
                                       self.volatility(),
                                       94.31186/106,
                                       0.25, 1.25,
                                       self.dfs()[0], self.dfs()[2]),
                               0.43, 2)

        self.assertAlmostEqual(CBO(OptionType.PUT, np.array([6, 106]),
                                   100.0, 0.25, np.array([0.75, 1.25]), 0.5,
                                   self.dfs()[0], self.dfs()[1:], self.dfs()[1],
                                   self.reversion(), self.volatility()),
                               0.44, 2)


if __name__ == '__main__':
    unittest.main()

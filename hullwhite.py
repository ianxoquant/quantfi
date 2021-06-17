import numpy as np
"""Hull White cap and swaption calculators"""
"""After Brigo/Mercurio Second Edition pp71-77"""


def AtT(r, a, v, T, t):
    pass


def BtT(a, T, t):
    if a > 0:
        return(1.0/a*(1.0 - np.exp(-a*(T-t))))
    elif a == 0.0:  # TODO should be an eps test?
        return(T-t)
    else:
        # TODO check if this is correct
        return((1.0/a*(1.0 - np.exp(-a*(T-t)))))


def PtT(r, a, v, T, t):
    pass


def VtT(a, v, T, t):
    """Price volatility of a zero coupon bond"""
    v * BtT(a, T, t) * np.sqrt(0.5*BtT(a, 2*T, 2*t))


def ZB():
    pass


def BO():
    pass

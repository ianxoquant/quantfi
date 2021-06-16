import numpy as np
"""Hull White cap and swaption calculators"""
"""After Brigo/Mercurio"""


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
    pass


def ZB():
    pass


def BO():
    pass

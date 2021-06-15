import numpy as np
from scipy.stats import norm

from globals import OptionType


# TODO move numerical method to a passed argument (numerical_method=ANALYTIC),
# add numerical integration and monte carlo
# allow np array arguments
def black_by_analytic(option_type, strike, forward,
                      expiration, volatility, discount_factor):
    """Returns option premium using Black model and lognormal volatility."""
    if not isinstance(option_type, OptionType):
        raise TypeError('option_type must be an instance of OptionType Enum')

    if strike <= 0. or forward <= 0. or expiration <= 0. or volatility <= 0.:
        return 0.

    if option_type == OptionType.FORWARD:
        premium = discount_factor * (forward - strike)
    else:
        d1 = (np.log(forward/strike) +
              volatility**2.0 * expiration/2.0) / (volatility * expiration**0.5)
        d2 = d1 - volatility * expiration**0.5

        premium = discount_factor * \
            (forward * norm.cdf(option_type*d1) -
             strike * norm.cdf(option_type*d2))
        if option_type == OptionType.PUT:
            premium = premium*option_type

    return premium


def bachelier_by_analytic(option_type, strike, forward,
                          expiration, volatility, discount_factor):
    """Returns option premium using the Bachelier model
       and normal volatility."""

    if not isinstance(option_type, OptionType):
        raise TypeError('option_type must be an instance of OptionType Enum')

    if expiration <= 0. or volatility <= 0.:
        return 0.

    if option_type == OptionType.FORWARD:
        premium = discount_factor * (forward - strike)
    else:
        d1 = (forward - strike) / (volatility * expiration**0.5)
        premium = discount_factor * (
            option_type * (forward - strike) * norm.cdf(option_type * d1) +
            volatility * (expiration / (2.0 * np.pi))**0.5 * np.exp(-d1**2.0 / 2.0))
    return premium

# unit tests
# assert premium values
# assert put-call parity
# check domain/range of each variable

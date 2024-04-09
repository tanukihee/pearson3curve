"""`pearson3curve`: Pearson Type III Curve Fitting and Plotting

`pearson3curve` is a Python package for curve fitting and plotting of data
points which follow the Pearson type III (P-III) distribution. It is useful in
hydrologic frequency analysis and hydraulic calculations.
"""

__VERSION__ = "0.7.0"

from pearson3curve.data import Data
from pearson3curve.curve import Curve
from pearson3curve.fitting import get_moments, get_fitted_moments

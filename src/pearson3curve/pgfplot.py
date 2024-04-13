"""The module for plotting the Pearson Type III distribution curve, using pgf
backend for better multi-language text and math typesetting support.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use("pgf")
plt.rcParams["pgf.rcfonts"] = False

from pearson3curve.plot import *


def set_tex_preamble(preamble: str) -> None:
    """Set the TeX preamble.

    Parameters
    ----------
    preamble : str
        The TeX preamble.
    """

    plt.rcParams["pgf.preamble"] = preamble


del show
del set_font

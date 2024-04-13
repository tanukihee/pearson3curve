"""The module for plotting the Pearson Type III distribution curve."""

from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import probscale  # type: ignore # pylint: disable=unused-import

from pearson3curve.curve import Curve
from pearson3curve.data import Data  # type: ignore # pylint: disable=unused-import

# Default parameters
_xlim: list[float] = [0, 100]


# Initialize the figure and axis
_fig = plt.figure(1)
_ax = _fig.add_subplot()

# Some pre-settings
_fig.set_layout_engine("constrained")
_ax.set_xscale("prob")
_ax.set_xlim(*_xlim)
_ax.grid(True)

_ax.set_xlabel("Frequency (%)")
_ax.set_ylabel("Flow (m³/s)")


def set_figsize(width: float, height: float) -> None:
    """Set the figure size.

    Parameters
    ----------
    width : float
        The width of the figure in inches.
    height : float
        The height of the figure in inches.
    """

    _fig.set_size_inches(width, height)


def set_font(font: str) -> None:
    """Set the font for text.

    Parameters
    ----------
    font : str
        The font name.
    """

    matplotlib.rcParams["font.sans-serif"] = font


def set_title(title: str, **kwargs) -> None:
    """Set the title of the plot.

    Parameters
    ----------
    title : str
        The title.
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.set_title`
    """

    _ax.set_title(title, **kwargs)


def set_xlim(left: float, right: float, **kwargs) -> None:
    """Set the x-axis limits.

    Parameters
    ----------
    left : float
        The left limit.
    right : float
        The right limit.
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.set_xlim`
    """

    _ax.set_xlim(left, right, **kwargs)
    _xlim[:] = [left, right]


def set_xlabel(label: str, **kwargs) -> None:
    """Set the x-axis label.

    Parameters
    ----------
    label : str
        The label.
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.set_xlabel`
    """

    _ax.set_xlabel(label, **kwargs)


def set_ylabel(label: str, **kwargs) -> None:
    """Set the y-axis label.

    Parameters
    ----------
    label : str
        The label.
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.set_ylabel`
    """

    _ax.set_ylabel(label, **kwargs)


def grid(visible: bool, **kwargs) -> None:
    """Set whether to show the grid.

    Parameters
    ----------
    visible : bool
        Whether to show the grid.
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.grid`
    """

    _ax.grid(visible, **kwargs)


def legend(**kwargs) -> None:
    """Set whether to show the legend.

    Parameters
    ----------
    **kwargs
        Additional keyword arguments to pass to the
        `matplotlib.axes.Axes.legend`
    """

    _ax.legend(**kwargs)


def scatter(
    data: Data,
    *,
    extreme_label="Extreme data",
    ordinary_label="Ordinary data",
    extreme_kwargs: dict[str, Any] | None = None,
    ordinary_kwargs: dict[str, Any] | None = None,
    **kwargs,
) -> None:
    """Plot the data as a scatter plot.

    Parameters
    ----------
    data : Data
        The data.
    extreme_label : str, optional
        The label for the extreme data, by default "Extreme data".
    ordinary_label : str, optional
        The label for the ordinary data, by default "Ordinary data".
    extreme_kwargs : dict[str, Any]
        Additional keyword arguments to pass to the `matplotlib.pyplot.scatter`
        for plotting the extreme data scatter points.
    ordinary_kwargs : dict[str, Any]
        Additional keyword arguments to pass to the `matplotlib.pyplot.scatter`
        for plotting the ordinary data scatter points.
    **kwargs
        Additional keyword arguments to pass to the `matplotlib.pyplot.scatter`
        for plotting the scatter points. If given, it will update both the
        `extreme_kwargs` and `ordinary_kwargs`.
    """

    def get_prob_lim(prob: float) -> float:
        if prob > 1:
            return 1

        return 10 ** np.ceil(np.log10(prob * 100) - 1)

    set_xlim(
        get_prob_lim(data.empirical_prob[0]),
        100 - get_prob_lim(100 - data.empirical_prob[-1]),
    )

    if extreme_kwargs is None:
        extreme_kwargs = {
            "marker": "x",
            "c": "k",
            "label": extreme_label,
        }

    if ordinary_kwargs is None:
        ordinary_kwargs = {
            "marker": "o",
            "c": "none",
            "edgecolors": "k",
            "label": ordinary_label,
        }

    if kwargs:
        extreme_kwargs.update(kwargs)
        ordinary_kwargs.update(kwargs)

    if len(data.extreme_data):
        plt.rcParams["scatter.marker"] = "x"
        _ax.scatter(data.extreme_prob * 100, data.extreme_data, **extreme_kwargs)

    plt.rcParams["scatter.marker"] = "o"
    _ax.scatter(data.ordinary_prob * 100, data.ordinary_data, **ordinary_kwargs)


def plot(
    curve: Curve,
    *,
    label: str | None = None,
    color: str | None = None,
    linestyle: str | None = None,
    linewidth: float | None = None,
    **kwargs,
) -> None:
    """Plot the Pearson Type III distribution curve.

    Parameters
    ----------
    curve : Curve
        The Pearson Type III distribution curve.
    label : str | None, optional
        The label for the curve, by default None. This will be passed to the
        `matplotlib.pyplot.plot`.
    color : str | None, optional
        The color of the curve, by default None. This will be passed to the
        `matplotlib.pyplot.plot`.
    linestyle : str | None, optional
        The line style of the curve, by default None. This will be passed to
        the `matplotlib.pyplot.plot`.
    linewidth : float | None, optional
        The line width of the curve, by default None. This will be passed to
        the `matplotlib.pyplot.plot`.
    **kwargs
        Additional keyword arguments to pass to the `matplotlib.pyplot.plot`.
    """

    kwargs.update(
        {"label": label, "color": color, "linestyle": linestyle, "linewidth": linewidth}
    )

    def create_space(lim: float) -> np.ndarray:
        if lim < 1:
            return np.concatenate(
                [
                    np.logspace(np.log10(lim), np.log10(1), num=200, endpoint=False),
                    np.logspace(np.log10(1), np.log10(10), num=150, endpoint=False),
                ]
            )

        return np.logspace(np.log10(lim), np.log10(10), num=350, endpoint=False)

    x1 = create_space(_xlim[0])
    x2 = (100 - create_space(100 - _xlim[1]))[::-1]
    x = np.concatenate([x1, np.linspace(10, 90, num=300), x2])
    y = [curve.get_value_from_prob(prob / 100) for prob in x]

    _ax.plot(x, y, **kwargs)


def show() -> None:
    """Display the plot."""

    _fig.show()


def save(file_name: str, *, transparent=True, dpi=300, **kwargs) -> None:
    """Save the plot to a file.

    Parameters
    ----------
    file_name : str
        File name.
    transparent : bool, optional
        Whether to save the plot with a transparent background, by default True.
    dpi : int, optional
        The resolution in dots per inch, by default 300.
    **kwargs
        Additional keyword arguments to pass to the `matplotlib.pyplot.savefig`
    """

    kwargs.update({"transparent": transparent, "dpi": dpi})

    _fig.savefig(file_name, **kwargs)

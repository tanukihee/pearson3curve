"""
The curve fitting module
"""

import numpy as np
from scipy import stats  # type: ignore
from scipy.optimize import curve_fit  # type: ignore

from pearson3curve import Curve, Data


def get_moments(data: Data) -> tuple[float, float, float]:
    """Get the P-III distribution moments (mean, coefficient of variation, and
    skewness) of the data.

    Parameters
    ----------
    data : Data
        The P-III distributed data.

    Returns
    -------
    tuple[float, float, float]
        The P-III moments (ex, cv, cs) of the data.
    """

    if len(data.extreme_data) == 0:
        mean = np.mean(data.data)
        variance: float = stats.variation(data.data, ddof=1)
        skewness: float = stats.skew(data.data, bias=False)
    else:
        r = (data.period_length - len(data.extreme_data)) / len(data.ordinary_data)

        mean = (
            np.sum(data.extreme_data) + r * np.sum(data.ordinary_data)
        ) / data.period_length

        variance = (
            np.sqrt(
                (
                    np.sum((data.extreme_data - mean) ** 2)
                    + r * np.sum((data.ordinary_data - mean) ** 2)
                )
                / (data.period_length - 1)
            )
            / mean
        )

        skewness = (
            data.period_length
            * (
                np.sum((data.extreme_data - mean) ** 3)
                + r * np.sum((data.ordinary_data - mean) ** 3)
            )
            / (
                (data.period_length - 1)
                * (data.period_length - 2)
                * mean**3
                * variance**3
            )
        )

    return mean, variance, skewness


def get_fitted_moments(
    data: Data,
    *,
    sv_ratio: float | None = None,
    fit_ex=True,
    moments: tuple[float, float, float] | None = None,
) -> tuple[float, float, float]:
    """Get the fitted P-III distribution moments (mean, coefficient of
    variation, and skewness) of the data.

    Parameters
    ----------
    data : Data
        The P-III distributed data.
    sv_ratio : float | None, optional
        The skewness-to-variance ratio, by default `None`, which means the
        variance and skewness will be fitted separately. If set, the skewness
        will be the product of the variance and the ratio.
    fit_ex : bool, optional
        Whether to fit the mean, by default True. If `False`, the mean will
        not be fitted.
    moments : tuple[float, float, float] | None, optional
        The moments (ex, cv, cs) of the data. If `None`, the moments will be
        calculated from the data.

    Returns
    -------
    tuple[float, float, float]
        The fitted P-III moments (ex, cv, cs) of the data.
    """

    if moments is None:
        m_ex, m_cv, m_cs = get_moments(data)
    else:
        m_ex, m_cv, m_cs = moments

    if sv_ratio is None:
        if fit_ex:
            popt = curve_fit(
                lambda prob, ex, cv, cs: Curve(ex, cv, cs).get_value_from_prob(prob),
                data.empirical_prob,
                data.data,
                p0=[m_ex, m_cv, m_cs],
            )[0]

            [ex, cv, cs] = popt
        else:
            popt = curve_fit(
                lambda prob, cv, cs: Curve(m_ex, cv, cs).get_value_from_prob(prob),
                data.empirical_prob,
                data.data,
                p0=[m_cv, m_cs],
            )[0]

            ex = m_ex
            [cv, cs] = popt
    else:
        if fit_ex:
            popt = curve_fit(
                lambda prob, ex, cv: Curve(ex, cv, cv * sv_ratio).get_value_from_prob(
                    prob
                ),
                data.empirical_prob,
                data.data,
                p0=[m_ex, m_cv],
            )[0]

            [ex, cv] = popt
            cs = cv * sv_ratio
        else:
            popt = curve_fit(
                lambda prob, cv: Curve(m_ex, cv, cv * sv_ratio).get_value_from_prob(
                    prob
                ),
                data.empirical_prob,
                data.data,
                p0=[m_cv],
            )[0]

            ex = m_ex
            [cv] = popt
            cs = cv * sv_ratio

    return ex, cv, cs

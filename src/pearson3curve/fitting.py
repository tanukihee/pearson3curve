"""
The curve fitting module
"""

import numpy as np
from scipy import stats  # type: ignore
from scipy.optimize import curve_fit  # type: ignore

from pearson3curve import Curve, DataSequence


def get_moments(sequence: DataSequence) -> tuple[float, float, float]:
    """Get the P-III distribution moments (mean, coefficient of variation, and
    skewness) of the data sequence.

    Parameters
    ----------
    sequence : DataSequence
        The data sequence.

    Returns
    -------
    tuple[float, float, float]
        The P-III moments (ex, cv, cs) of the data sequence.
    """

    if len(sequence.extreme_data) == 0:
        mean = np.mean(sequence.data)
        variance: float = stats.variation(sequence.data, ddof=1)
        skewness: float = stats.skew(sequence.data, bias=False)
    else:
        r = (sequence.period_length - len(sequence.extreme_data)) / len(
            sequence.ordinary_data
        )

        mean = (
            np.sum(sequence.extreme_data) + r * np.sum(sequence.ordinary_data)
        ) / sequence.period_length

        variance = (
            np.sqrt(
                np.sum((sequence.extreme_data - mean) ** 2)
                + r
                * np.sum((sequence.ordinary_data - mean) ** 2)
                / (sequence.period_length - 1)
            )
            / mean
        )

        skewness = sequence.period_length * np.sum(
            (sequence.extreme_data - mean) ** 3
        ) + r * np.sum((sequence.ordinary_data - mean) ** 3) / (
            (sequence.period_length - 1)
            * (sequence.period_length - 2)
            * mean**3
            * variance**3
        )

    return mean, variance, skewness


def get_fitted_moments(
    sequence: DataSequence,
    *,
    sv_ratio: float | None = None,
    fit_ex=True,
    moments: tuple[float, float, float] | None = None,
) -> tuple[float, float, float]:
    """Get the fitted P-III distribution moments (mean, coefficient of
    variation, and skewness) of the data sequence.

    Parameters
    ----------
    sequence : DataSequence
        The data sequence.
    sv_ratio : float | None, optional
        The skewness-to-variance ratio, by default `None`, which means the
        variance and skewness are fitted separately. If set, the skewness will
        be the product of the variance and the ratio.
    fit_ex : bool, optional
        Whether to fit the mean, by default `True`. If `False`, the mean will
        not be fitted.
    moments : tuple[float, float, float] | None, optional
        The moments (ex, cv, cs) of the data sequence. If `None`, the moments
        will be calculated from the data sequence.

    Returns
    -------
    tuple[float, float, float]
        The fitted P-III parameters (ex, cv, cs) of the data sequence.
    """

    if moments is None:
        m_ex, m_cv, m_cs = get_moments(sequence)
    else:
        m_ex, m_cv, m_cs = moments

    if sv_ratio is None:
        if fit_ex:
            popt = curve_fit(
                lambda prob, ex, cv, cs: Curve(ex, cv, cs).get_value_from_prob(prob),
                sequence.empirical_prob,
                sequence.data,
                p0=[m_ex, m_cv, m_cs],
            )[0]

            [ex, cv, cs] = popt
        else:
            popt = curve_fit(
                lambda prob, cv, cs: Curve(m_ex, cv, cs).get_value_from_prob(prob),
                sequence.empirical_prob,
                sequence.data,
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
                sequence.empirical_prob,
                sequence.data,
                p0=[m_ex, m_cv],
            )[0]

            [ex, cv] = popt
            cs = cv * sv_ratio
        else:
            popt = curve_fit(
                lambda prob, cv: Curve(m_ex, cv, cv * sv_ratio).get_value_from_prob(
                    prob
                ),
                sequence.empirical_prob,
                sequence.data,
                p0=[m_cv],
            )[0]

            ex = m_ex
            [cv] = popt
            cs = cv * sv_ratio

    return ex, cv, cs

import math
import statistics

from scipy import stats  # type: ignore
from scipy.stats import pearson3  # type: ignore
from scipy.optimize import curve_fit  # type: ignore

from pearson3curve import DataSequence


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
        mean = statistics.mean(sequence.data)
        variance: float = stats.variation(sequence.data, ddof=1)
        skewness: float = stats.skew(sequence.data, bias=False)
    else:
        r = (sequence.period_length - len(sequence.extreme_data)) / len(
            sequence.ordinary_data
        )

        mean = (
            sum(sequence.extreme_data) + r * sum(sequence.ordinary_data)
        ) / sequence.period_length

        variance = (
            math.sqrt(
                (
                    sum((x - mean) ** 2 for x in sequence.extreme_data)
                    + r * sum((x - mean) ** 2 for x in sequence.ordinary_data)
                )
                / (sequence.period_length - 1)
            )
            / mean
        )

        skewness = (
            sequence.period_length
            * (
                sum((x - mean) ** 3 for x in sequence.extreme_data)
                + r * sum((x - mean) ** 3 for x in sequence.ordinary_data)
            )
            / (
                (sequence.period_length - 1)
                * (sequence.period_length - 2)
                * mean**3
                * variance**3
            )
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

    def p3_curve(prob: float, ex: float, cv: float, cs: float) -> float:
        return (pearson3.ppf(1 - prob, cs) * cv + 1) * ex

    if sv_ratio is None:
        if fit_ex:
            popt = curve_fit(
                p3_curve, sequence.empirical_prob, sequence.data, p0=[m_ex, m_cv, m_cs]
            )[0]

            [ex, cv, cs] = popt
        else:
            popt = curve_fit(
                lambda prob, cv, cs: p3_curve(prob, m_ex, cv, cs),
                sequence.empirical_prob,
                sequence.data,
                p0=[m_cv, m_cs],
            )[0]

            ex = m_ex
            [cv, cs] = popt
    else:
        if fit_ex:
            popt = curve_fit(
                lambda prob, ex, cv: p3_curve(prob, ex, cv, cv * sv_ratio),
                sequence.empirical_prob,
                sequence.data,
                p0=[m_ex, m_cv],
            )[0]

            [ex, cv] = popt
            cs = cv * sv_ratio
        else:
            popt = curve_fit(
                lambda prob, cv: p3_curve(prob, m_ex, cv, cv * sv_ratio),
                sequence.empirical_prob,
                sequence.data,
                p0=[m_cv],
            )[0]

            ex = m_ex
            [cv] = popt
            cs = cv * sv_ratio

    return ex, cv, cs

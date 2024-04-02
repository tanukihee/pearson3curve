"""`pearson3curve`: Pearson Type III Curve Fitting and Plotting

`pearson3curve` is a Python package for curve fitting and plotting of data
points which follow the Pearson type III (P-III) distribution. It is useful in
hydrologic frequency analysis and hydraulic calculations.
"""

__VERSION__ = "0.7.0"


from typing import Sequence

import numpy as np
from scipy.stats import pearson3  # type: ignore


class DataSequence:
    """The class for the data sequence."""

    def __init__(self, observed_data: list[float] | np.ndarray) -> None:
        """The constructor of the DataSequence class.

        Parameters
        ----------
        observed_data : list[float] | np.ndarray
            The observed data sequence, supporting either a list or a numpy
            array.
        """

        if isinstance(observed_data, list):
            self._observed_data = np.array(observed_data)
        else:
            self._observed_data = observed_data

        self._data = np.sort(self._observed_data)[::-1]
        self._extreme_data = np.array([])
        self._ordinary_data = self._data.copy()
        self._period_length = len(observed_data)

        self._empirical_prob: np.ndarray | None = None

    @property
    def data(self) -> np.ndarray:
        """The sorted data sequence.

        Returns
        -------
        np.ndarray
            The sorted data sequence.
        """

        return self._data

    @property
    def extreme_data(self) -> np.ndarray:
        """The sorted ordinary data sequence.

        Returns
        -------
        Sequence[float]
            The sorted ordinary data sequence.
        """

        return self._extreme_data

    @property
    def ordinary_data(self) -> np.ndarray:
        """The sorted ordinary data sequence.

        Returns
        -------
        np.ndarray
            The sorted ordinary data sequence.
        """

        return self._ordinary_data

    @property
    def period_length(self) -> int:
        """The survey period length for the data sequence.

        Returns
        -------
        int
            The survey period length for the data sequence.
        """

        return self._period_length

    def set_history_data(
        self,
        history_data: list[float] | np.ndarray,
        period_length: int,
        *,
        extreme_num: int | None = None,
    ):
        """Set the history data and the survey period length if needed.

        Parameters
        ----------
        history_data : list[float] | np.ndarray
            The history data sequence, supporting either a list or a numpy
            array.
        period_length : int
            The survey period length.
        extreme_num : int | None, optional
            The number of extreme data, by default None. If `None`, all the
            history data will be treated as extreme data.

        Raises
        ------
        ValueError
            * If the period length is less than the sum of the lengths of the
            observed data and the history data.
            * If the number of extreme data is less than the length of the
            history data.
        """

        if period_length < len(self._observed_data) + len(history_data):
            raise ValueError(
                "The period length should not be less than the sum of the \
lengths of the observed data and the history data."
            )

        self._period_length = period_length

        if extreme_num is None:
            extreme_num = len(history_data)

        if extreme_num < len(history_data):
            raise ValueError(
                "The number of extreme data should not be less than the length \
of the history data."
            )

        self._data = np.sort(np.concatenate([self._observed_data, history_data]))[::-1]
        self._extreme_data = self._data[:extreme_num]
        self._ordinary_data = self._data[extreme_num:]

    @property
    def extreme_prob(self) -> np.ndarray:
        """The empirical probability sequence for the extreme data.

        Returns
        -------
        Sequence[float]
            The empirical probability sequence for the extreme data.
        """

        if self._empirical_prob is not None:
            return self._empirical_prob[: len(self.extreme_data)]

        if (l := len(self.extreme_data)) == 0:
            return np.array([])

        return (np.arange(l) + 1) / (self._period_length + 1)

    @property
    def ordinary_prob(self) -> np.ndarray:
        """The empirical probability sequence for the ordinary data."""
        if self._empirical_prob is not None:
            return self._empirical_prob[len(self.extreme_data) :]

        if len(self.extreme_data) == 0:
            return (np.arange(self._period_length) + 1) / (self._period_length + 1)

        ep = self.extreme_prob[-1]
        lo = len(self.ordinary_data)
        return ep + (1 - ep) * (np.arange(lo) + 1) / (lo + 1)

    @property
    def empirical_prob(self) -> np.ndarray:
        """The empirical probability sequence."""
        if self._empirical_prob is not None:
            return self._empirical_prob

        return np.concatenate([self.extreme_prob, self.ordinary_prob])

    def set_empirical_prob(self, empirical_prob: list[float] | np.ndarray) -> None:
        """Set the full empirical probability sequence.

        Parameters
        ----------
        empirical_prob : list[float] | np.ndarray
            The empirical probability sequence, supporting either a list or a
            numpy array. The length should be the same as the length of the data
            sequence. And the values should be in the range from 0 to 1.

        Raises
        ------
        ValueError
            * If the length of the empirical probability sequence is not the
            same as the length of the data sequence.
            * If any value in the empirical probability sequence is out of the
            range from 0 to 1.
        """

        if len(empirical_prob) != len(self.data):
            raise ValueError(
                "The length of the empirical probability sequence should be \
same as the survey period length."
            )

        if any(p < 0 or p > 1 for p in empirical_prob):
            raise ValueError(
                "The values in the empirical probability sequence should be in \
the range from 0 to 1."
            )

        if isinstance(empirical_prob, list):
            self._empirical_prob = np.array(empirical_prob)
        else:
            self._empirical_prob = empirical_prob

    def set_empirical_prob_by_order(
        self, order: int, prob: float, *, start_value=1
    ) -> None:
        """Set the empirical probability by the order number of the data.

        Parameters
        ----------
        order : int
            The order number of the data sequence, starting from `start_value`,
            which is 1 by default. The data sequence is sorted in descending
            order. Therefore, the first data is the largest one.
        prob : float
            The empirical probability to be set. It should be in the range from
            0 to 1.
        start_value : int, optional
            The start number of the order, by default 1.

        Raises
        ------
        IndexError
            If the order number is out of the range of the data sequence.

        ValueError
            If the probability is out of the range from 0 to 1.
        """

        if order < start_value or order > len(self.data) - 1 + start_value:
            raise IndexError(
                "The order number is out of the range of the data sequence."
            )

        if prob < 0 or prob > 1:
            raise ValueError("The probability should be in the range from 0 to 1.")

        ep = self.empirical_prob.copy()
        self._empirical_prob = np.where(
            np.arange(len(ep)) == order - start_value, prob, ep
        )


class Curve:
    """The P-III distribution curve."""

    def __init__(self, ex: float, cv: float, cs: float):
        """Initialize the P-III distribution curve.

        Parameters
        ----------
        ex : float
            The mean of the distribution.
        cv : float
            The coefficient of variation of the distribution.
        cs : float
            The skewness of the distribution.
        """
        self.ex = ex
        self.cv = cv
        self.cs = cs

    def get_value_from_prob(self, prob: float) -> float:
        """Get the value from the probability.

        Parameters
        ----------
        prob : float
            The probability, from 0 to 1.

        Returns
        -------
        float
            The value. `nan` if the probability is out of the range from 0 to 1.
        """
        return (pearson3.ppf(1 - prob, self.cs) * self.cv + 1) * self.ex

    def get_prob_from_value(self, value: float) -> float:
        """Get the probability from the value.

        Parameters
        ----------
        value : float
            The value.

        Returns
        -------
        float
            The probability, from 0 to 1.
        """
        return 1 - pearson3.cdf((value / self.ex - 1) / self.cv, self.cs)

"""`pearson3curve`: Pearson Type III Curve Fitting and Plotting

`pearson3curve` is a Python package for curve fitting and plotting of data
points which follow the Pearson type III (P-III) distribution. It is useful in
hydrologic frequency analysis and hydraulic calculations.
"""

__VERSION__ = "0.7.0"


from typing import Sequence


class DataSequence:
    """The class for the data sequence."""

    def __init__(self, observed_data: list[float]) -> None:
        """The constructor of the DataSequence class.

        Parameters
        ----------
        observed_data : list[float]
            The observed data sequence.
        """

        self._observed_data = observed_data
        self._data = sorted(observed_data, reverse=True)
        self._extreme_data: list[float] = []
        self._ordinary_data = self._data
        self._period_length = len(observed_data)

        self._empirical_prob: list[float] | None = None

    @property
    def data(self) -> Sequence[float]:
        """The sorted data sequence."""

        return self._data

    @property
    def extreme_data(self) -> Sequence[float]:
        """The sorted ordinary data sequence."""

        return self._extreme_data

    @property
    def ordinary_data(self) -> Sequence[float]:
        """The sorted ordinary data sequence."""

        return self._ordinary_data

    @property
    def period_length(self) -> int:
        """The survey period length for the data sequence."""

        return self._period_length

    def set_history_data(
        self,
        history_data: list[float],
        period_length: int,
        *,
        extreme_num: int | None = None,
    ):
        """Set the history data and the survey period length if needed.

        Parameters
        ----------
        history_data : list[float]
            The history data sequence.
        period_length : int
            The survey period length.
        extreme_num : int | None, optional
            The number of extreme data.

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
        elif extreme_num < len(history_data):
            raise ValueError(
                "The number of extreme data should not be less than the length \
of the history data."
            )

        self._data = sorted(self._observed_data + history_data, reverse=True)
        self._extreme_data = self._data[:extreme_num]
        self._ordinary_data = self._data[extreme_num:]

    @property
    def empirical_prob(self) -> Sequence[float]:
        """The empirical probability sequence."""
        if self._empirical_prob is not None:
            return self._empirical_prob

        return list(self.extreme_prob) + list(self.ordinary_prob)

    @property
    def extreme_prob(self) -> Sequence[float]:
        """The empirical probability sequence for the extreme data."""
        if self._empirical_prob is not None:
            return self._empirical_prob[: len(self.extreme_data)]

        if (l := len(self.extreme_data)) == 0:
            return []

        return [
            (i + 1) / (self._period_length + 1)
            for i in range(self._period_length)
            if i < l
        ]

    @property
    def ordinary_prob(self) -> Sequence[float]:
        """The empirical probability sequence for the ordinary data."""
        if self._empirical_prob is not None:
            return self._empirical_prob[len(self.extreme_data) :]

        if len(self.extreme_data) == 0:
            return [
                (i + 1) / (self._period_length + 1) for i in range(self._period_length)
            ]

        ep = self.extreme_prob[-1]
        lo = len(self.ordinary_data)
        return [ep + (1 - ep) * (i + 1) / (lo + 1) for i in range(lo)]

    def set_empirical_prob(self, empirical_prob: list[float]) -> None:
        """Set the full empirical probability sequence.

        Parameters
        ----------
        empirical_prob : list[float]
            The empirical probability sequence. The length should be the same as
            the length of the data sequence.

        Raises
        ------
        ValueError
            If the length of the empirical probability sequence is not the same
            as the length of the data sequence.
        """

        if len(empirical_prob) != len(self.data):
            raise ValueError(
                "The length of the empirical probability sequence should be \
same as the survey period length."
            )

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
            The empirical probability to be set.
        start_value : int, optional
            The start number of the order, by default 1.

        Raises
        ------
        IndexError
            If the order number is out of the range of the data sequence.
        """

        if order < start_value or order > len(self.data) - 1 + start_value:
            raise IndexError(
                "The order number is out of the range of the data sequence."
            )

        ep = self.empirical_prob
        self._empirical_prob = [
            prob if i == order - start_value else ep[i] for i in range(len(ep))
        ]

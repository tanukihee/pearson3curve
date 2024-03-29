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

    @property
    def data(self) -> Sequence[float]:
        """The sorted data sequence.

        Returns
        -------
        Sequence[float]
            The ordinary data sequence.
        """

        return self._data

    @property
    def extreme_data(self) -> Sequence[float]:
        """The sorted ordinary data sequence.

        Returns
        -------
        Sequence[float]
            The sorted ordinary data sequence.
        """

        return self._extreme_data

    @property
    def ordinary_data(self) -> Sequence[float]:
        """The sorted ordinary data sequence.

        Returns
        -------
        Sequence[float]
            The sorted ordinary data sequence.
        """

        return self._ordinary_data

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
        return list(self.extreme_prob) + list(self.ordinary_prob)

    @property
    def extreme_prob(self) -> Sequence[float]:
        """The empirical probability sequence for the extreme data."""
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
        if len(self.extreme_data) == 0:
            return [
                (i + 1) / (self._period_length + 1) for i in range(self._period_length)
            ]

        ep = self.extreme_prob[-1]
        lo = len(self.ordinary_data)
        return [ep + (1 - ep) * (i + 1) / (lo + 1) for i in range(lo)]

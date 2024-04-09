"""The P-III distribution curve class."""

from scipy.stats import pearson3  # type: ignore


class Curve:
    """The P-III distribution curve class."""

    def __init__(self, ex: float, cv: float, cs: float):
        """Initialize the P-III distribution curve from the moments.

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

import numpy as np
import pytest

from pearson3curve import Data, get_moments


def test_successive_momentum_params():
    d = Data(np.random.rand(100).tolist())

    ex, cv, cs = get_moments(d)

    e = np.sum(d.data) / len(d.data)
    assert ex == pytest.approx(e)

    s = np.sqrt(np.sum((d.data - ex) ** 2) / (len(d.data) - 1))
    v = s / ex
    assert cv == pytest.approx(v)

    n = len(d.data)
    sk = n * np.sum((d.data - ex) ** 3) / ((n - 1) * (n - 2) * ex**3 * cv**3)

    assert sk == pytest.approx(cs)

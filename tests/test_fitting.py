import numpy as np
import pytest

from pearson3curve import DataSequence
from pearson3curve.fitting import get_moments


def test_successive_momentum_params():
    ds = DataSequence(np.random.rand(100).tolist())

    ex, cv, cs = get_moments(ds)

    print(ex, cv, cs)

    e = np.sum(ds.data) / len(ds.data)
    assert ex == pytest.approx(e)

    s = np.sqrt(np.sum((ds.data - ex) ** 2) / (len(ds.data) - 1))
    v = s / ex
    assert cv == pytest.approx(v)

    n = len(ds.data)
    sk = n * np.sum((ds.data - ex) ** 3) / ((n - 1) * (n - 2) * ex**3 * cv**3)

    assert sk == pytest.approx(cs)

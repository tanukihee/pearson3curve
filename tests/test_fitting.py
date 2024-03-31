import math

import numpy as np
import pytest

from pearson3curve import DataSequence
from pearson3curve.fitting import get_moments


def test_successive_momentum_params():
    ds = DataSequence(np.random.rand(100).tolist())

    ex, cv, cs = get_moments(ds)

    print(ex, cv, cs)

    e = sum(ds.data) / len(ds.data)
    assert ex == pytest.approx(e)

    s = math.sqrt(sum((x - ex) ** 2 for x in ds.data) / (len(ds.data) - 1))
    v = s / ex
    assert cv == pytest.approx(v)

    n = len(ds.data)
    sk = n * sum((x - ex) ** 3 for x in ds.data) / ((n - 1) * (n - 2) * ex**3 * cv**3)

    assert sk == pytest.approx(cs)

import math
import pytest

from pearson3curve import Curve


def test_curve():
    curve = Curve(100, 1, 2)

    assert curve.get_value_from_prob(0.01) == pytest.approx(460.517019)
    assert curve.get_value_from_prob(0.5) == pytest.approx(69.314718)
    assert curve.get_value_from_prob(0.99) == pytest.approx(1.005034)

    assert math.isnan(curve.get_value_from_prob(2))

    assert curve.get_prob_from_value(50) == pytest.approx(0.60653066)
    assert curve.get_prob_from_value(100) == pytest.approx(0.36787944)
    assert curve.get_prob_from_value(200) == pytest.approx(0.13533528)

import pytest

from pearson3curve import Data


@pytest.fixture
def d() -> Data:
    return Data([1, 2, 3])


def test_data_sequence(d: Data) -> None:
    assert d.data == pytest.approx([3, 2, 1])


def test_set_history_data(d: Data) -> None:
    d.set_history_data([6], 6)
    assert d.data == pytest.approx([6, 3, 2, 1])
    assert d.extreme_data == pytest.approx([6])
    assert d.ordinary_data == pytest.approx([3, 2, 1])

    with pytest.raises(ValueError):
        d.set_history_data([6], 3)


def test_set_history_data_with_extreme_num(d: Data) -> None:
    d.set_history_data([6], 6, extreme_num=2)
    assert d.data == pytest.approx([6, 3, 2, 1])
    assert d.extreme_data == pytest.approx([6, 3])
    assert d.ordinary_data == pytest.approx([2, 1])

    with pytest.raises(ValueError):
        d.set_history_data([4, 5, 6], 6, extreme_num=2)


def test_empirical_prob(d: Data) -> None:
    assert d.ordinary_prob == pytest.approx([0.25, 0.5, 0.75])
    assert d.extreme_prob == pytest.approx([])
    assert d.empirical_prob == pytest.approx([0.25, 0.5, 0.75])

    d.set_history_data([10], 9)
    assert d.extreme_prob == pytest.approx([0.1])
    assert d.ordinary_prob == pytest.approx([0.325, 0.55, 0.775])
    assert d.empirical_prob == pytest.approx([0.1, 0.325, 0.55, 0.775])

    d2 = Data([1, 2, 3, 4])
    d2.set_history_data([10], 9, extreme_num=2)
    assert d2.extreme_prob == pytest.approx([0.1, 0.2])
    assert d2.ordinary_prob == pytest.approx([0.4, 0.6, 0.8])
    assert d2.empirical_prob == pytest.approx([0.1, 0.2, 0.4, 0.6, 0.8])


def test_set_empirical_prob(d: Data) -> None:
    empirical_prob = [0.1, 0.2, 0.3]
    d.set_empirical_prob(empirical_prob)
    assert d.empirical_prob == pytest.approx(empirical_prob)

    with pytest.raises(ValueError):
        d.set_empirical_prob([0.1, 0.2])

    with pytest.raises(ValueError):
        d.set_empirical_prob([0.1, 0.2, 2])


def test_set_empirical_prob_by_no(d: Data) -> None:
    d.set_empirical_prob_by_order(2, 0.4)
    assert d.empirical_prob == pytest.approx([0.25, 0.4, 0.75])

    d.set_empirical_prob_by_order(0, 0.2, start_value=0)
    assert d.empirical_prob == pytest.approx([0.2, 0.4, 0.75])

    with pytest.raises(IndexError):
        d.set_empirical_prob_by_order(0, 0.4)

    with pytest.raises(IndexError):
        d.set_empirical_prob_by_order(4, 0.4)

    with pytest.raises(IndexError):
        d.set_empirical_prob_by_order(3, 0.4, start_value=0)

    with pytest.raises(ValueError):
        d.set_empirical_prob_by_order(2, 2)


def test_set_empirical_prob_by_no_with_history_data(d: Data) -> None:
    d.set_history_data([10], 9)
    d.set_empirical_prob_by_order(2, 0.4)
    assert d.empirical_prob == pytest.approx([0.1, 0.4, 0.55, 0.775])
    assert d.extreme_prob == pytest.approx([0.1])
    assert d.ordinary_prob == pytest.approx([0.4, 0.55, 0.775])

    d2 = Data([1, 2, 3, 4])
    d2.set_history_data([10], 9, extreme_num=2)
    d2.set_empirical_prob_by_order(1, 0.05)
    assert d2.empirical_prob == pytest.approx([0.05, 0.2, 0.4, 0.6, 0.8])
    assert d2.extreme_prob == pytest.approx([0.05, 0.2])
    assert d2.ordinary_prob == pytest.approx([0.4, 0.6, 0.8])

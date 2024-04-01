import pytest

from pearson3curve import DataSequence


@pytest.fixture
def ds() -> DataSequence:
    return DataSequence([1, 2, 3])


def test_data_sequence(ds: DataSequence) -> None:
    assert ds.data == [3, 2, 1]


def test_set_history_data(ds: DataSequence) -> None:
    ds.set_history_data([6], 6)
    assert ds.data == [6, 3, 2, 1]
    assert ds.extreme_data == [6]
    assert ds.ordinary_data == [3, 2, 1]

    with pytest.raises(ValueError):
        ds.set_history_data([6], 3)


def test_set_history_data_with_extreme_num(ds: DataSequence) -> None:
    ds.set_history_data([6], 6, extreme_num=2)
    assert ds.data == [6, 3, 2, 1]
    assert ds.extreme_data == [6, 3]
    assert ds.ordinary_data == [2, 1]

    with pytest.raises(ValueError):
        ds.set_history_data([4, 5, 6], 6, extreme_num=2)


def test_empirical_prob(ds: DataSequence) -> None:
    assert ds.ordinary_prob == [0.25, 0.5, 0.75]
    assert ds.extreme_prob == []
    assert ds.empirical_prob == [0.25, 0.5, 0.75]

    ds.set_history_data([10], 9)
    assert ds.extreme_prob == [0.1]
    assert ds.ordinary_prob == [0.325, 0.55, 0.775]
    assert ds.empirical_prob == [0.1, 0.325, 0.55, 0.775]

    ds2 = DataSequence([1, 2, 3, 4])
    ds2.set_history_data([10], 9, extreme_num=2)
    assert ds2.extreme_prob == [0.1, 0.2]
    assert ds2.ordinary_prob == pytest.approx([0.4, 0.6, 0.8])
    assert ds2.empirical_prob == pytest.approx([0.1, 0.2, 0.4, 0.6, 0.8])


def test_set_empirical_prob(ds: DataSequence) -> None:
    empirical_prob = [0.1, 0.2, 0.3]
    ds.set_empirical_prob(empirical_prob)
    assert ds.empirical_prob == empirical_prob

    with pytest.raises(ValueError):
        ds.set_empirical_prob([0.1, 0.2])

    with pytest.raises(ValueError):
        ds.set_empirical_prob([0.1, 0.2, 2])


def test_set_empirical_prob_by_no(ds: DataSequence) -> None:
    ds.set_empirical_prob_by_order(2, 0.4)
    assert ds.empirical_prob == [0.25, 0.4, 0.75]

    ds.set_empirical_prob_by_order(0, 0.2, start_value=0)
    assert ds.empirical_prob == [0.2, 0.4, 0.75]

    with pytest.raises(IndexError):
        ds.set_empirical_prob_by_order(0, 0.4)

    with pytest.raises(IndexError):
        ds.set_empirical_prob_by_order(4, 0.4)

    with pytest.raises(IndexError):
        ds.set_empirical_prob_by_order(3, 0.4, start_value=0)

    with pytest.raises(ValueError):
        ds.set_empirical_prob_by_order(2, 2)


def test_set_empirical_prob_by_no_with_history_data(ds: DataSequence) -> None:
    ds.set_history_data([10], 9)
    ds.set_empirical_prob_by_order(2, 0.4)
    assert ds.empirical_prob == [0.1, 0.4, 0.55, 0.775]
    assert ds.extreme_prob == [0.1]
    assert ds.ordinary_prob == [0.4, 0.55, 0.775]

    ds2 = DataSequence([1, 2, 3, 4])
    ds2.set_history_data([10], 9, extreme_num=2)
    ds2.set_empirical_prob_by_order(1, 0.05)
    assert ds2.empirical_prob == pytest.approx([0.05, 0.2, 0.4, 0.6, 0.8])
    assert ds2.extreme_prob == [0.05, 0.2]
    assert ds2.ordinary_prob == pytest.approx([0.4, 0.6, 0.8])

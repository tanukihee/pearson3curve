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


def test_set_history_data_with_small_period_data(ds: DataSequence) -> None:
    with pytest.raises(ValueError):
        ds.set_history_data([6], 3)


def test_set_history_data_with_extreme_num(ds: DataSequence) -> None:
    ds.set_history_data([6], 6, extreme_num=2)
    assert ds.data == [6, 3, 2, 1]
    assert ds.extreme_data == [6, 3]
    assert ds.ordinary_data == [2, 1]


def test_set_history_data_with_small_extreme_num(ds: DataSequence) -> None:
    with pytest.raises(ValueError):
        ds.set_history_data([4, 5, 6], 6, extreme_num=2)


def test_empirical_prob(ds: DataSequence) -> None:
    assert ds.ordinary_prob == [0.25, 0.5, 0.75]
    assert ds.extreme_prob == []
    assert ds.empirical_prob == [0.25, 0.5, 0.75]


def test_empirical_prob_with_history_data(ds: DataSequence) -> None:
    ds.set_history_data([10], 9)
    assert ds.extreme_prob == [0.1]
    assert ds.ordinary_prob == [0.325, 0.55, 0.775]
    assert ds.empirical_prob == [0.1, 0.325, 0.55, 0.775]


def test_empirical_prob_with_history_data_and_extreme_num() -> None:
    ds2 = DataSequence([1, 2, 3, 4])
    ds2.set_history_data([10], 9, extreme_num=2)
    assert ds2.extreme_prob == [0.1, 0.2]
    assert ds2.ordinary_prob == pytest.approx([0.4, 0.6, 0.8])
    assert ds2.empirical_prob == pytest.approx([0.1, 0.2, 0.4, 0.6, 0.8])

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

# The API Documentation for `pearson3curve`

## `pearson3curve` Module

### `Data` Class

```python
class Data
```

The P-III distributed data class.

---

#### Methods

```python
def __init__(self, observed_data: list[float] | np.ndarray) -> None
```

Initialize the P-III distributed data from the observed data.

- Parameters

  - `observed_data` : `list[float] | np.ndarray`

    The observed data, supporting either a list or a numpy array.

---

```python
def set_history_data(
    self,
    history_data: list[float] | np.ndarray,
    period_length: int,
    *,
    extreme_num: int | None = None,
) -> None
```

Set the history data and the survey period length.

- Parameters:

  - `history_data` : `list[float] | np.ndarray`

    The history data, supporting either a list or a numpy array.

  - `period_length` : `int`

    The survey period length.

  - `extreme_num` : `int | None`, optional

    The number of extreme data, by default None. If `None`, all the history data will be treated as extreme data.

- Raises:

  - `ValueError`

    - If the period length is less than the sum of the lengths of the observed data and the history data.

    - If the number of extreme data is less than the length of the history data.

---

```python
def set_empirical_prob(self, empirical_prob: list[float] | np.ndarray) -> None
```

Set all the empirical probabilities for the data.

- Parameters:

  - `empirical_prob` : `list[float] | np.ndarray`

    The total empirical probabilities, supporting either a list or a numpy array. The length should be the same as the length of the data. And the values should be in the range from 0 to 1.

- Raises:

  - `ValueError`

    - If the length of the empirical probabilities is not the same as the length of the data.

    - If any value in the empirical probabilities is out of the range from 0 to 1.

---

```python
def set_empirical_prob_by_order(
    self, order: int, prob: float, *, start_value=1
) -> None
```

Set the empirical probability of the data by the order number.

- Parameters:

  - `order` : `int`

    The order number of the data, starting from `start_value`, which is 1 by default. The data is sorted in descending order. Therefore, the first data is the largest one.

  - `prob` : `float`

    The empirical probability to be set. It should be in the range from 0 to 1.

  - `start_value` : `int`, optional

    The start number of the order, by default 1.

- Raises:

  - `IndexError`

    If the order number is out of the range of the data.

  - `ValueError`

    If the empirical probability is out of the range from 0 to 1.

---

#### Properties

```python
@property
def data(self) -> np.ndarray
```

The descending sorted data.

---

```python
@property
def extreme_data(self) -> np.ndarray
```

The descending sorted extreme data.

---

```python
@property
def ordinary_data(self) -> np.ndarray
```

The descending sorted ordinary data.

---

```python
@property
def period_length(self) -> int
```

The survey period length of the data.

---

```python
@property
def extreme_prob(self) -> np.ndarray
```

The empirical probabilities of the extreme data.

---

```python
@property
def ordinary_prob(self) -> np.ndarray
```

The empirical probabilities of the ordinary data.

---

```python
@property
def empirical_prob(self) -> np.ndarray
```

The empirical probabilities for the data.

### `Curve` Class

```python
class Curve
```

The P-III distributed curve class.

---

#### Methods

```python
def __init__(self, ex: float, cv: float, cs: float) -> None
```

Initialize the P-III distributed curve from the moments.

- Parameters

  - `ex` : `float`

    The mean of the distribution.

  - `cv` : `float`

    The coefficient of variation of the distribution.

  - `cs` : `float`

    The skewness of the distribution.

---

```python
def get_value_from_prob(self, prob: float) -> float
```

Get the value from the probability.

- Parameters

  - `prob` : `float`

    The probability, from 0 to 1.

- Returns

  - `float`

    The value. `nan` if the probability is out of the range from 0 to 1.

---

```python
def get_prob_from_value(self, value: float) -> float
```

Get the probability from the value.

- Parameters

  - `value` : `float`

    The value.

- Returns

  - `float`

    The probability, from 0 to 1.

### `get_moments` Function

```python
def get_moments(data: Data) -> tuple[float, float, float]
```

Get the P-III distribution moments (mean, coefficient of variation, and skewness) of the data.

- Parameters

  - `data` : `Data`

    The P-III distributed data.

- Returns

  - `tuple[float, float, float]`

    The moments (ex, cv, cs) of the data.

### `get_fitted_moments` Function

```python
def get_fitted_moments(
    data: Data,
    *,
    sv_ratio: float | None = None,
    fit_ex=True,
    moments: tuple[float, float, float] | None = None,
) -> tuple[float, float, float]
```

Get the fitted P-III distribution moments (mean, coefficient of variation, and skewness) of the data.

- Parameters

  - `data` : `Data`

    The P-III distributed data.

  - `sv_ratio` : `float | None`, optional

    The skewness-to-variance ratio, by default `None`, which means the variance and skewness will be fitted separately. If set, the skewness will be the product of the variance and the ratio.

  - `fit_ex` : `bool`, optional

    Whether to fit the mean, by default True. If `False`, the mean will not be fitted.

  - `moments` : `tuple[float, float, float] | None`, optional

    The moments (ex, cv, cs) of the data. If `None`, the moments will be calculated from the data.

- Returns

  - `tuple[float, float, float]`

    The fitted P-III moments (ex, cv, cs) of the data.

## `pearson3curve.plot` and `pearson3curve.pgfplot` Modules

The module for plotting the Pearson Type III distribution curve. The `pgfplot` module uses pgf
backend for better multi-language text and math typesetting support.

### `set_figsize` Function

```python
def set_figsize(width: float, height: float) -> None
```

Set the figure size.

- Parameters

  - `width` : `float`

    The width of the figure in inches.

  - `height` : `float`

    The height of the figure in inches.

### `set_font` Function

```python
def set_font(font: str) -> None
```

Set the font for the plot. Only available for the `plot` module.

- Parameters

  - `font` : `str`

    The font name.

### `set_tex_preamble` Function

```python
def set_tex_preamble(preamble: str) -> None
```

Set the TeX preamble. Only available for the `pgfplot` module.

- Parameters

  - `preamble` : `str`

    The TeX preamble.

### `set_title` Function

```python
def set_title(title: str, **kwargs) -> None
```

Set the title of the plot.

- Parameters

  - `title` : `str`

    The title.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.set_title` method.

### `set_xlim` Function

```python
def set_xlim(left: float, right: float, **kwargs) -> None
```

Set the x-axis limits.

- Parameters

  - `left` : `float`

    The left limit.

  - `right` : `float`

    The right limit.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.set_xlim` method.

### `set_xlabel` Function

```python
def set_xlabel(label: str, **kwargs) -> None
```

Set the x-axis label.

- Parameters

  - `label` : `str`

    The label.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.set_xlabel` method.

### `set_ylabel` Function

```python
def set_ylabel(label: str, **kwargs) -> None
```

Set the y-axis label.

- Parameters

  - `label` : `str`

    The label.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.set_ylabel` method.

### `grid` Function

```python
def grid(visible: bool, **kwargs) -> None
```

Set whether to show the grid.

- Parameters

  - `visible` : `bool`

    Whether to show the grid.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.grid` method.

### `legend` Function

```python
def legend(**kwargs) -> None
```

Set whether to show the legend.

- Parameters

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.axes.Axes.legend` method.

### `scatter` Function

```python
def scatter(
    data: Data,
    *,
    extreme_label="Extreme data",
    ordinary_label="Ordinary data",
    extreme_kwargs: dict[str, Any] | None = None,
    ordinary_kwargs: dict[str, Any] | None = None,
    **kwargs,
) -> None
```

Plot the scatter plot of the data.

- Parameters

  - `data` : `Data`

    The data.

  - `extreme_label` : `str`, optional

    The label for the extreme data, by default "Extreme data".

  - `ordinary_label` : `str`, optional

    The label for the ordinary data, by default "Ordinary data".

  - `extreme_kwargs` : `dict[str, Any] | None`, optional

    Additional keyword arguments to be passed to the `matplotlib.pyplot.scatter` function for plotting the extreme data scatter points, by default None.

  - `ordinary_kwargs` : `dict[str, Any] | None`, optional

    Additional keyword arguments to be passed to the `matplotlib.pyplot.scatter` function for plotting the ordinary data scatter points, by default None.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.pyplot.scatter` function. If given, it will update both the `extreme_kwargs` and `ordinary_kwargs`.

### `plot` Function

```python
def plot(
    curve: Curve,
    *,
    label: str | None = None,
    color: str | None = None,
    linestyle: str | None = None,
    linewidth: float | None = None,
    **kwargs,
) -> None
```

Plot the Pearson Type III distribution curve.

- Parameters

  - `curve` : `Curve`

    The Pearson Type III distribution curve.

  - `label` : `str | None`, optional

    The label for the curve, by default None.

  - `color` : `str | None`, optional

    The color for the curve, by default None.

  - `linestyle` : `str | None`, optional

    The line style for the curve, by default None.

  - `linewidth` : `float | None`, optional

    The line width for the curve, by default None.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.pyplot.plot` function.

### `show` Function

```python
def show() -> None
```

Show the plot. Only available for the `plot` module.

### `save` Function

```python
def save(file_name: str, *, transparent=True, dpi=300, **kwargs) -> None
```

Save the plot to a file.

- Parameters

  - `file_name` : `str`

    The file name.

  - `transparent` : `bool`, optional

    Whether to save the plot with a transparent background, by default True.

  - `dpi` : `int`, optional

    The resolution in dots per inch, by default 300. This will be omitted if saving to a vector format.

  - `**kwargs`

    Additional keyword arguments to be passed to the `matplotlib.figure.Figure.savefig` method.

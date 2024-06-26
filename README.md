# `pearson3curve`: Pearson Type III Curve Fitting and Plotting

`pearson3curve` is a Python package for curve fitting and plotting of data
points which follow the Pearson type III (P-III) distribution. It is useful in
hydrologic frequency analysis and hydraulic calculations.

Notice: This package is the brand new version of the old `Pearson3CurveFitting`
package. For the old version, please refer to the
[archived repository](https://github.com/tanukihee/Pearson3CurveFittingArchive).

## Installation

```bash
pip install pearson3curve
```

## Usages

See [API Documentation](https://github.com/tanukihee/pearson3curve/blob/main/docs/api.md) for details.

## Examples

### Successive Data

See [Successive Data Example](https://github.com/tanukihee/pearson3curve/blob/main/example/successive.py) for the code.

Figure example:

<img src="https://raw.githubusercontent.com/tanukihee/pearson3curve/main/example/successive.png" width="100%" alt="successive"/>

### Non-Successive Data

See [Non-Successive Data Example](https://github.com/tanukihee/pearson3curve/blob/main/example/nonsuccessive.py) for the code.

Figure example in Chinese, using pgf backend for better multi-language text and
math typesetting support:

<img src="https://raw.githubusercontent.com/tanukihee/pearson3curve/main/example/nonsuccessive.svg" width="100%" alt="nonsuccessive"/>

## Development

This package uses `pdm` for package management. For detailed usages, please
refer to the [pdm documentation](https://pdm-project.org/en/latest/).

---

Copyright (c) 2020 -- 2024 ListLee

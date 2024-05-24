"""Tests for Bollinger."""
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["ishanpai"]
__all__ = []

import numpy as np
import pytest

from sktime.datasets import load_airline
from sktime.transformations.series.bollinger import Bollinger


@pytest.mark.parametrize("window", [2, 12])
@pytest.mark.parametrize("k", [1, 5])
def test_bollinger_against_raw_implementation(window, k):
    y = load_airline()
    t = Bollinger(window=window, k=k)
    y_t = t.fit_transform(y)

    ma = y.rolling(window=window).mean()
    std = y.rolling(window=window).std()

    np.testing.assert_array_equal(
        y_t.xs("moving_average", axis=1, level=0).values, ma.values
    )
    np.testing.assert_array_equal(
        y_t.xs("upper", axis=1, level=0).values, (ma + k * std).values
    )
    np.testing.assert_array_equal(
        y_t.xs("lower", axis=1, level=0).values, (ma - k * std).values
    )


@pytest.mark.parametrize("window", [1, 12])
@pytest.mark.parametrize("k", [1, 0])
def test_bollinger_input_error(window, k):
    with pytest.raises(ValueError):
        Bollinger(window=window, k=k)

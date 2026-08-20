import pytest

from app.services.analytics import _stats


def test_empirical_quantiles_interpolate_discrete_pairs() -> None:
    result = _stats([float(value) for value in range(20)])

    assert result["mean"] == 9.5
    assert result["p10"] == pytest.approx(1.9)
    assert result["p90"] == pytest.approx(17.1)
    assert result["valid_count"] == 20


def test_empirical_p90_can_be_below_mean_with_upper_outlier() -> None:
    result = _stats([1.0] * 19 + [100.0])

    assert result["mean"] > result["p90"]

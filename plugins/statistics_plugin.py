"""Statistical operations plugin for Math CLI using SciPy."""

from core.base_operations import MathOperation
import numpy as np
from scipy import stats
import math


class MeanOperation(MathOperation):
    """Calculate arithmetic mean of numbers."""

    name = "mean"
    args = ["*values"]
    help = "Calculate mean: mean 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate mean.

        Args:
            *values: Numbers to average

        Returns:
            Arithmetic mean
        """
        if len(values) == 0:
            raise ValueError("Need at least one value")
        return float(np.mean(values))


class MedianOperation(MathOperation):
    """Calculate median of numbers."""

    name = "median"
    args = ["*values"]
    help = "Calculate median: median 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate median.

        Args:
            *values: Numbers

        Returns:
            Median value
        """
        if len(values) == 0:
            raise ValueError("Need at least one value")
        return float(np.median(values))


class ModeOperation(MathOperation):
    """Calculate mode (most common value) of numbers."""

    name = "mode"
    args = ["*values"]
    help = "Calculate mode: mode 1 2 2 3 3 3"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate mode.

        Args:
            *values: Numbers

        Returns:
            Most common value
        """
        if len(values) == 0:
            raise ValueError("Need at least one value")
        mode_result = stats.mode(values, keepdims=True)
        return float(mode_result.mode[0])


class StandardDeviationOperation(MathOperation):
    """Calculate standard deviation."""

    name = "stdev"
    args = ["*values"]
    help = "Calculate standard deviation: stdev 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate standard deviation.

        Args:
            *values: Numbers

        Returns:
            Standard deviation (sample)
        """
        if len(values) < 2:
            raise ValueError("Need at least two values")
        return float(np.std(values, ddof=1))  # Sample std dev


class VarianceOperation(MathOperation):
    """Calculate variance."""

    name = "variance"
    args = ["*values"]
    help = "Calculate variance: variance 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate variance.

        Args:
            *values: Numbers

        Returns:
            Variance (sample)
        """
        if len(values) < 2:
            raise ValueError("Need at least two values")
        return float(np.var(values, ddof=1))  # Sample variance


class RangeOperation(MathOperation):
    """Calculate range (max - min)."""

    name = "range"
    args = ["*values"]
    help = "Calculate range: range 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate range.

        Args:
            *values: Numbers

        Returns:
            max - min
        """
        if len(values) == 0:
            raise ValueError("Need at least one value")
        return float(max(values) - min(values))


class PercentileOperation(MathOperation):
    """Calculate percentile."""

    name = "percentile"
    args = ["percentile", "*values"]
    help = "Calculate percentile: percentile 75 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, percentile: float, *values) -> float:
        """Calculate percentile.

        Args:
            percentile: Percentile to calculate (0-100)
            *values: Numbers

        Returns:
            Value at given percentile
        """
        if len(values) == 0:
            raise ValueError("Need at least one value")
        if not 0 <= percentile <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        return float(np.percentile(values, percentile))


class CorrelationOperation(MathOperation):
    """Calculate Pearson correlation coefficient between two datasets."""

    name = "correlation"
    args = ["n", "*values"]
    help = "Calculate correlation: correlation 3 x1 x2 x3 y1 y2 y3"
    category = "statistics"

    @classmethod
    def execute(cls, n: int, *values) -> float:
        """Calculate correlation.

        Args:
            n: Number of pairs
            *values: x values followed by y values

        Returns:
            Pearson correlation coefficient
        """
        if len(values) != 2 * n:
            raise ValueError(f"Expected {2*n} values (n x values and n y values)")
        if n < 2:
            raise ValueError("Need at least 2 pairs")

        x = np.array(values[:n])
        y = np.array(values[n:])

        corr, _ = stats.pearsonr(x, y)
        return float(corr)


class CovarianceOperation(MathOperation):
    """Calculate covariance between two datasets."""

    name = "covariance"
    args = ["n", "*values"]
    help = "Calculate covariance: covariance 3 x1 x2 x3 y1 y2 y3"
    category = "statistics"

    @classmethod
    def execute(cls, n: int, *values) -> float:
        """Calculate covariance.

        Args:
            n: Number of pairs
            *values: x values followed by y values

        Returns:
            Covariance
        """
        if len(values) != 2 * n:
            raise ValueError(f"Expected {2*n} values")
        if n < 2:
            raise ValueError("Need at least 2 pairs")

        x = np.array(values[:n])
        y = np.array(values[n:])

        return float(np.cov(x, y)[0, 1])


class ZScoreOperation(MathOperation):
    """Calculate z-score for a value."""

    name = "zscore"
    args = ["value", "*population"]
    help = "Calculate z-score: zscore 10 5 6 7 8 9 10 11"
    category = "statistics"

    @classmethod
    def execute(cls, value: float, *population) -> float:
        """Calculate z-score.

        Args:
            value: Value to calculate z-score for
            *population: Population values

        Returns:
            Z-score
        """
        if len(population) < 2:
            raise ValueError("Need at least 2 population values")

        mean = np.mean(population)
        std = np.std(population, ddof=1)

        if std == 0:
            raise ValueError("Standard deviation is zero")

        return float((value - mean) / std)


class QuartileOperation(MathOperation):
    """Calculate quartiles (Q1, Q2/median, Q3)."""

    name = "quartiles"
    args = ["*values"]
    help = "Calculate quartiles: quartiles 1 2 3 4 5 6 7 8 9"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> tuple:
        """Calculate quartiles.

        Args:
            *values: Numbers

        Returns:
            Tuple of (Q1, Q2, Q3)
        """
        if len(values) < 4:
            raise ValueError("Need at least 4 values")

        q1 = np.percentile(values, 25)
        q2 = np.percentile(values, 50)
        q3 = np.percentile(values, 75)

        return (float(q1), float(q2), float(q3))


class IQROperation(MathOperation):
    """Calculate interquartile range (IQR)."""

    name = "iqr"
    args = ["*values"]
    help = "Calculate IQR: iqr 1 2 3 4 5 6 7 8 9"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate IQR.

        Args:
            *values: Numbers

        Returns:
            Interquartile range (Q3 - Q1)
        """
        if len(values) < 4:
            raise ValueError("Need at least 4 values")

        return float(stats.iqr(values))


class SkewnessOperation(MathOperation):
    """Calculate skewness of a dataset."""

    name = "skewness"
    args = ["*values"]
    help = "Calculate skewness: skewness 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate skewness.

        Args:
            *values: Numbers

        Returns:
            Skewness value
        """
        if len(values) < 3:
            raise ValueError("Need at least 3 values")

        return float(stats.skew(values))


class KurtosisOperation(MathOperation):
    """Calculate kurtosis of a dataset."""

    name = "kurtosis"
    args = ["*values"]
    help = "Calculate kurtosis: kurtosis 1 2 3 4 5"
    category = "statistics"

    @classmethod
    def execute(cls, *values) -> float:
        """Calculate kurtosis.

        Args:
            *values: Numbers

        Returns:
            Kurtosis value
        """
        if len(values) < 4:
            raise ValueError("Need at least 4 values")

        return float(stats.kurtosis(values))


class NormalCDFOperation(MathOperation):
    """Calculate normal distribution CDF."""

    name = "normal_cdf"
    args = ["x", "mean", "std"]
    help = "Calculate P(X <= x) for normal: normal_cdf 1.5 0 1"
    category = "statistics"

    @classmethod
    def execute(cls, x: float, mean: float, std: float) -> float:
        """Calculate normal CDF.

        Args:
            x: Value
            mean: Mean of distribution
            std: Standard deviation

        Returns:
            P(X <= x)
        """
        if std <= 0:
            raise ValueError("Standard deviation must be positive")

        return float(stats.norm.cdf(x, mean, std))


class NormalPDFOperation(MathOperation):
    """Calculate normal distribution PDF."""

    name = "normal_pdf"
    args = ["x", "mean", "std"]
    help = "Calculate normal PDF at x: normal_pdf 0 0 1"
    category = "statistics"

    @classmethod
    def execute(cls, x: float, mean: float, std: float) -> float:
        """Calculate normal PDF.

        Args:
            x: Value
            mean: Mean of distribution
            std: Standard deviation

        Returns:
            PDF value at x
        """
        if std <= 0:
            raise ValueError("Standard deviation must be positive")

        return float(stats.norm.pdf(x, mean, std))


class TTestOperation(MathOperation):
    """Perform one-sample t-test."""

    name = "ttest"
    args = ["mu", "*values"]
    help = "One-sample t-test: ttest 5 4 5 6 7 8"
    category = "statistics"

    @classmethod
    def execute(cls, mu: float, *values) -> tuple:
        """Perform one-sample t-test.

        Args:
            mu: Hypothesized mean
            *values: Sample values

        Returns:
            Tuple of (t-statistic, p-value)
        """
        if len(values) < 2:
            raise ValueError("Need at least 2 sample values")

        t_stat, p_value = stats.ttest_1samp(values, mu)
        return (float(t_stat), float(p_value))


class LinearRegressionOperation(MathOperation):
    """Calculate linear regression (y = mx + b)."""

    name = "linear_regression"
    args = ["n", "*values"]
    help = "Linear regression: linear_regression 3 x1 x2 x3 y1 y2 y3"
    category = "statistics"

    @classmethod
    def execute(cls, n: int, *values) -> tuple:
        """Calculate linear regression.

        Args:
            n: Number of points
            *values: x values followed by y values

        Returns:
            Tuple of (slope, intercept, r_value, p_value, std_err)
        """
        if len(values) != 2 * n:
            raise ValueError(f"Expected {2*n} values")
        if n < 2:
            raise ValueError("Need at least 2 points")

        x = np.array(values[:n])
        y = np.array(values[n:])

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        return (float(slope), float(intercept), float(r_value), float(p_value), float(std_err))


# All operations are automatically discovered by the plugin manager

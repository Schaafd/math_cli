"""Advanced plotting utilities for statistical visualizations.

This module extends the basic ASCII plotting with:
- Histograms
- Box plots
- Scatter plots with regression lines
- Heatmaps
- Distribution plots
"""

import pandas as pd
import numpy as np
from typing import List, Union, Optional, Tuple
from utils.plotting import ASCIIPlotter


class StatisticalPlotter:
    """Advanced plotting for statistical data visualization."""

    def __init__(self, width: int = 60, height: int = 20):
        """Initialize the statistical plotter.

        Args:
            width: Plot width in characters
            height: Plot height in characters
        """
        self.width = width
        self.height = height
        self.plotter = ASCIIPlotter(width=width, height=height)

    def histogram(self, data: Union[List[float], pd.Series, np.ndarray],
                  bins: int = 10) -> str:
        """Create a histogram.

        Args:
            data: Data to plot
            bins: Number of bins

        Returns:
            ASCII histogram
        """
        # Convert to numpy array
        if isinstance(data, pd.Series):
            data = data.values
        elif isinstance(data, list):
            data = np.array(data)

        # Remove NaN values
        data = data[~np.isnan(data)]

        if len(data) == 0:
            return "Error: No valid data"

        # Create histogram
        counts, edges = np.histogram(data, bins=bins)

        # Create bar chart from histogram
        result = []
        result.append(f"Histogram ({bins} bins)")
        result.append("─" * self.width)

        # Find max count for scaling
        max_count = max(counts)
        bar_width = self.width - 20

        # Plot each bin
        for i, (count, edge) in enumerate(zip(counts, edges[:-1])):
            # Calculate bar length
            bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0

            # Format label
            next_edge = edges[i + 1]
            label = f"{edge:8.2f}-{next_edge:8.2f}"

            # Create bar
            bar = "█" * bar_len
            result.append(f"{label} │{bar} {count}")

        result.append("─" * self.width)
        result.append(f"Min: {data.min():.2f}, Max: {data.max():.2f}, "
                     f"Mean: {data.mean():.2f}, Std: {data.std():.2f}")

        return "\n".join(result)

    def boxplot(self, data: Union[List[float], pd.Series, np.ndarray],
                label: str = "Data") -> str:
        """Create a box plot showing quartiles and outliers.

        Args:
            data: Data to plot
            label: Label for the data

        Returns:
            ASCII box plot
        """
        # Convert to numpy array
        if isinstance(data, pd.Series):
            data = data.values
        elif isinstance(data, list):
            data = np.array(data)

        # Remove NaN values
        data = data[~np.isnan(data)]

        if len(data) == 0:
            return "Error: No valid data"

        # Calculate statistics
        q1 = np.percentile(data, 25)
        q2 = np.percentile(data, 50)  # median
        q3 = np.percentile(data, 75)
        iqr = q3 - q1

        # Calculate whiskers (1.5 * IQR)
        lower_whisker = q1 - 1.5 * iqr
        upper_whisker = q3 + 1.5 * iqr

        # Find actual whisker values
        lower_actual = data[data >= lower_whisker].min()
        upper_actual = data[data <= upper_whisker].max()

        # Find outliers
        outliers = data[(data < lower_whisker) | (data > upper_whisker)]

        # Create visualization
        result = []
        result.append(f"Box Plot: {label}")
        result.append("─" * self.width)

        # Scale to plot width
        data_range = data.max() - data.min()
        plot_width = self.width - 20

        def scale(val):
            return int(((val - data.min()) / data_range) * plot_width)

        # Create the box plot
        plot_line = [" "] * plot_width

        # Mark positions
        q1_pos = scale(q1)
        q2_pos = scale(q2)
        q3_pos = scale(q3)
        lower_pos = scale(lower_actual)
        upper_pos = scale(upper_actual)

        # Draw whiskers
        if lower_pos < q1_pos:
            for i in range(lower_pos, q1_pos):
                plot_line[i] = "─"
            plot_line[lower_pos] = "├"

        # Draw box
        for i in range(q1_pos, q3_pos + 1):
            if i == q1_pos:
                plot_line[i] = "├"
            elif i == q2_pos:
                plot_line[i] = "│"
            elif i == q3_pos:
                plot_line[i] = "┤"
            elif plot_line[i] == " ":
                plot_line[i] = "─"

        # Draw upper whisker
        if upper_pos > q3_pos:
            for i in range(q3_pos + 1, min(upper_pos + 1, plot_width)):
                plot_line[i] = "─"
            if upper_pos < plot_width:
                plot_line[upper_pos] = "┤"

        # Mark outliers with 'o'
        for outlier in outliers:
            pos = scale(outlier)
            if 0 <= pos < plot_width:
                plot_line[pos] = "o"

        result.append("          " + "".join(plot_line))
        result.append("─" * self.width)

        # Statistics
        result.append(f"Min: {data.min():.2f}  Q1: {q1:.2f}  Median: {q2:.2f}  "
                     f"Q3: {q3:.2f}  Max: {data.max():.2f}")
        result.append(f"IQR: {iqr:.2f}  Outliers: {len(outliers)}")

        return "\n".join(result)

    def scatter_with_regression(self, x: Union[List[float], pd.Series, np.ndarray],
                                y: Union[List[float], pd.Series, np.ndarray]) -> str:
        """Create scatter plot with linear regression line.

        Args:
            x: X values
            y: Y values

        Returns:
            ASCII scatter plot with regression line
        """
        # Convert to numpy arrays
        if isinstance(x, pd.Series):
            x = x.values
        elif isinstance(x, list):
            x = np.array(x)

        if isinstance(y, pd.Series):
            y = y.values
        elif isinstance(y, list):
            y = np.array(y)

        # Remove NaN pairs
        mask = ~(np.isnan(x) | np.isnan(y))
        x = x[mask]
        y = y[mask]

        if len(x) == 0:
            return "Error: No valid data"

        # Calculate regression line
        coefficients = np.polyfit(x, y, 1)
        slope, intercept = coefficients
        r_squared = np.corrcoef(x, y)[0, 1] ** 2

        # Create scatter plot
        result = []
        result.append(f"Scatter Plot with Linear Regression")
        result.append(f"y = {slope:.3f}x + {intercept:.3f}  (R² = {r_squared:.3f})")
        result.append("─" * self.width)

        # Create plot area
        plot_height = self.height
        plot_width = self.width

        # Scale data to plot dimensions
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()

        # Add padding
        x_range = x_max - x_min
        y_range = y_max - y_min
        x_min -= x_range * 0.05
        x_max += x_range * 0.05
        y_min -= y_range * 0.05
        y_max += y_range * 0.05

        def scale_x(val):
            return int(((val - x_min) / (x_max - x_min)) * (plot_width - 1))

        def scale_y(val):
            return plot_height - 1 - int(((val - y_min) / (y_max - y_min)) * (plot_height - 1))

        # Initialize plot grid
        grid = [[" " for _ in range(plot_width)] for _ in range(plot_height)]

        # Draw regression line
        for px in range(plot_width):
            x_val = x_min + (px / (plot_width - 1)) * (x_max - x_min)
            y_val = slope * x_val + intercept
            py = scale_y(y_val)
            if 0 <= py < plot_height:
                grid[py][px] = "─"

        # Plot data points (overwrite regression line)
        for xi, yi in zip(x, y):
            px = scale_x(xi)
            py = scale_y(yi)
            if 0 <= px < plot_width and 0 <= py < plot_height:
                grid[py][px] = "●"

        # Convert grid to string
        for row in grid:
            result.append("".join(row))

        result.append("─" * self.width)
        result.append(f"X: [{x.min():.2f}, {x.max():.2f}]  "
                     f"Y: [{y.min():.2f}, {y.max():.2f}]")

        return "\n".join(result)

    def heatmap(self, data: Union[pd.DataFrame, np.ndarray],
                labels: Optional[List[str]] = None) -> str:
        """Create a correlation heatmap.

        Args:
            data: 2D data (correlation matrix)
            labels: Optional row/column labels

        Returns:
            ASCII heatmap
        """
        # Convert to numpy array
        if isinstance(data, pd.DataFrame):
            if labels is None:
                labels = list(data.columns)
            data = data.values

        if data.ndim != 2:
            return "Error: Data must be 2D"

        rows, cols = data.shape

        # Create color mapping (using characters)
        def value_to_char(val):
            """Map value (-1 to 1) to character."""
            if np.isnan(val):
                return " "
            val = np.clip(val, -1, 1)
            chars = " .:-=+*#%@"
            idx = int((val + 1) / 2 * (len(chars) - 1))
            return chars[idx]

        result = []
        result.append("Correlation Heatmap")
        result.append("─" * self.width)

        # Add labels if provided
        if labels:
            label_width = max(len(str(label)) for label in labels) + 2

            for i, row in enumerate(data):
                row_label = str(labels[i])[:label_width-1].ljust(label_width)
                heatmap_row = " ".join(value_to_char(val) for val in row)
                result.append(f"{row_label}│ {heatmap_row}")
        else:
            for row in data:
                heatmap_row = " ".join(value_to_char(val) for val in row)
                result.append(heatmap_row)

        result.append("─" * self.width)
        result.append("Scale: -1.0 [  ] 0.0 [:-] +1.0 [@#]")

        return "\n".join(result)

    def distribution_plot(self, data: Union[List[float], pd.Series, np.ndarray]) -> str:
        """Create a distribution plot combining histogram and density.

        Args:
            data: Data to plot

        Returns:
            ASCII distribution plot
        """
        # Use histogram for now (could enhance with kernel density estimate)
        return self.histogram(data, bins=15)


# Convenience functions
def plot_histogram(data: Union[List[float], pd.Series, np.ndarray],
                   bins: int = 10, width: int = 60, height: int = 15) -> str:
    """Create a histogram plot.

    Args:
        data: Data to plot
        bins: Number of bins
        width: Plot width
        height: Plot height

    Returns:
        ASCII histogram
    """
    plotter = StatisticalPlotter(width=width, height=height)
    return plotter.histogram(data, bins=bins)


def plot_boxplot(data: Union[List[float], pd.Series, np.ndarray],
                 label: str = "Data", width: int = 60) -> str:
    """Create a box plot.

    Args:
        data: Data to plot
        label: Data label
        width: Plot width

    Returns:
        ASCII box plot
    """
    plotter = StatisticalPlotter(width=width, height=10)
    return plotter.boxplot(data, label=label)


def plot_scatter_regression(x: Union[List[float], pd.Series, np.ndarray],
                            y: Union[List[float], pd.Series, np.ndarray],
                            width: int = 60, height: int = 20) -> str:
    """Create scatter plot with regression.

    Args:
        x: X values
        y: Y values
        width: Plot width
        height: Plot height

    Returns:
        ASCII scatter plot with regression line
    """
    plotter = StatisticalPlotter(width=width, height=height)
    return plotter.scatter_with_regression(x, y)


def plot_heatmap(data: Union[pd.DataFrame, np.ndarray],
                 labels: Optional[List[str]] = None, width: int = 60) -> str:
    """Create a heatmap.

    Args:
        data: 2D data
        labels: Optional labels
        width: Plot width

    Returns:
        ASCII heatmap
    """
    plotter = StatisticalPlotter(width=width, height=20)
    return plotter.heatmap(data, labels=labels)

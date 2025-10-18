"""Plotting operations plugin for Math CLI.

Provides both basic plotting operations and statistical plotting
operations that integrate with loaded datasets.
"""

from core.base_operations import MathOperation
from utils.plotting import plot_function_string, plot_expression, ASCIIPlotter
from utils.data_io import get_data_manager
from utils.advanced_plotting import (
    plot_histogram,
    plot_boxplot,
    plot_scatter_regression,
    plot_heatmap
)
import pandas as pd
import numpy as np


class PlotFunctionOperation(MathOperation):
    """Plot a mathematical function over a range."""

    name = "plot"
    args = ["function", "start", "end"]
    help = "Plot a function over a range (e.g., plot sin 0 6.28)"

    @classmethod
    def execute(cls, function, start, end):
        """Execute the plot operation.

        Args:
            function: Function name (sin, cos, tan, exp, log, sqrt, square, cube, abs, inv)
            start: Start of x range
            end: End of x range

        Returns:
            ASCII plot string
        """
        # Convert function to string if it's numeric (error case)
        func_name = str(function) if isinstance(function, (int, float)) else function

        # Display the plot
        result = plot_function_string(func_name, start, end)

        # Print it directly for visual display
        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Plot:[/cyan] {func_name}(x) from {start} to {end}\n")
            console.print(result)
        else:
            print(f"\nPlot: {func_name}(x) from {start} to {end}\n")
            print(result)

        # Return a summary
        return f"Plotted {func_name}(x)"


class PlotDataOperation(MathOperation):
    """Plot data points."""

    name = "plot_data"
    args = ["values"]
    help = "Plot a series of data points (e.g., plot_data 10 20 15 30 25)"
    variadic = True

    @classmethod
    def execute(cls, *values):
        """Execute the plot data operation.

        Args:
            *values: Variable number of y values

        Returns:
            Summary string
        """
        if len(values) == 0:
            raise ValueError("plot_data requires at least one value")

        # Create plotter
        plotter = ASCIIPlotter(width=50, height=15)
        result = plotter.plot_data(list(values), style='scatter')

        # Display the plot
        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Data Plot:[/cyan] {len(values)} points\n")
            console.print(result)
        else:
            print(f"\nData Plot: {len(values)} points\n")
            print(result)

        # Return summary
        return f"Plotted {len(values)} data points"


class PlotBarOperation(MathOperation):
    """Plot data as a bar chart."""

    name = "plot_bar"
    args = ["values"]
    help = "Plot data as a bar chart (e.g., plot_bar 10 20 15 30 25)"
    variadic = True

    @classmethod
    def execute(cls, *values):
        """Execute the bar plot operation.

        Args:
            *values: Variable number of y values

        Returns:
            Summary string
        """
        if len(values) == 0:
            raise ValueError("plot_bar requires at least one value")

        # Create plotter
        plotter = ASCIIPlotter(width=min(len(values) * 4, 60), height=15)
        result = plotter.plot_data(list(values), style='bar')

        # Display the plot
        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Bar Chart:[/cyan] {len(values)} values\n")
            console.print(result)
        else:
            print(f"\nBar Chart: {len(values)} values\n")
            print(result)

        # Return summary
        return f"Plotted {len(values)} bars"


class PlotLineOperation(MathOperation):
    """Plot data as a line chart."""

    name = "plot_line"
    args = ["values"]
    help = "Plot data as a line chart (e.g., plot_line 10 20 15 30 25)"
    variadic = True

    @classmethod
    def execute(cls, *values):
        """Execute the line plot operation.

        Args:
            *values: Variable number of y values

        Returns:
            Summary string
        """
        if len(values) == 0:
            raise ValueError("plot_line requires at least one value")

        # Create plotter
        plotter = ASCIIPlotter(width=50, height=15)
        result = plotter.plot_data(list(values), style='line')

        # Display the plot
        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Line Chart:[/cyan] {len(values)} points\n")
            console.print(result)
        else:
            print(f"\nLine Chart: {len(values)} points\n")
            print(result)

        # Return summary
        return f"Plotted {len(values)} points as line"


# Statistical Plotting Operations (Phase 5.2.5)
# These operations integrate with DataManager for dataset-based plotting

class PlotHistogramOperation(MathOperation):
    """Create a histogram from dataset column."""

    name = "plot_hist"
    args = ["dataset", "column", "?bins"]
    help = "Plot histogram: plot_hist mydata price 20"
    category = "visualization"

    @classmethod
    def execute(cls, dataset: str, column: str, bins: str = "10") -> str:
        """Create histogram from dataset column.

        Args:
            dataset: Name of loaded dataset
            column: Column name to plot
            bins: Number of bins (default: 10)

        Returns:
            ASCII histogram
        """
        manager = get_data_manager()

        # Get dataset
        df = manager.get_dataset(dataset)

        # Validate column exists
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

        # Get column data
        data = df[column]

        # Validate numeric
        if not pd.api.types.is_numeric_dtype(data):
            raise ValueError(f"Column '{column}' must be numeric for histogram")

        # Convert bins to int
        try:
            bins_int = int(bins)
        except ValueError:
            raise ValueError(f"bins must be an integer, got: {bins}")

        # Create and display plot
        result = plot_histogram(data, bins=bins_int)

        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Histogram:[/cyan] {dataset}.{column}\n")
            console.print(result)
        else:
            print(f"\nHistogram: {dataset}.{column}\n")
            print(result)

        return f"Plotted histogram of {dataset}.{column}"


class PlotBoxplotOperation(MathOperation):
    """Create a box plot from dataset column."""

    name = "plot_box"
    args = ["dataset", "column", "?label"]
    help = "Plot box plot: plot_box mydata revenue Sales"
    category = "visualization"

    @classmethod
    def execute(cls, dataset: str, column: str, label: str = None) -> str:
        """Create box plot from dataset column.

        Args:
            dataset: Name of loaded dataset
            column: Column name to plot
            label: Optional label for the plot

        Returns:
            ASCII box plot
        """
        manager = get_data_manager()

        # Get dataset
        df = manager.get_dataset(dataset)

        # Validate column exists
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

        # Get column data
        data = df[column]

        # Validate numeric
        if not pd.api.types.is_numeric_dtype(data):
            raise ValueError(f"Column '{column}' must be numeric for box plot")

        # Use column name as label if not provided
        if label is None:
            label = column

        # Create and display plot
        result = plot_boxplot(data, label=label)

        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Box Plot:[/cyan] {dataset}.{column}\n")
            console.print(result)
        else:
            print(f"\nBox Plot: {dataset}.{column}\n")
            print(result)

        return f"Plotted box plot of {dataset}.{column}"


class PlotScatterOperation(MathOperation):
    """Create a scatter plot with regression line."""

    name = "plot_scatter"
    args = ["dataset", "x_column", "y_column"]
    help = "Plot scatter with regression: plot_scatter mydata quantity price"
    category = "visualization"

    @classmethod
    def execute(cls, dataset: str, x_column: str, y_column: str) -> str:
        """Create scatter plot with linear regression.

        Args:
            dataset: Name of loaded dataset
            x_column: Column name for x-axis
            y_column: Column name for y-axis

        Returns:
            ASCII scatter plot with regression line
        """
        manager = get_data_manager()

        # Get dataset
        df = manager.get_dataset(dataset)

        # Validate columns exist
        if x_column not in df.columns:
            raise ValueError(f"Column '{x_column}' not found. Available: {list(df.columns)}")
        if y_column not in df.columns:
            raise ValueError(f"Column '{y_column}' not found. Available: {list(df.columns)}")

        # Get column data
        x_data = df[x_column]
        y_data = df[y_column]

        # Validate numeric
        if not pd.api.types.is_numeric_dtype(x_data):
            raise ValueError(f"Column '{x_column}' must be numeric for scatter plot")
        if not pd.api.types.is_numeric_dtype(y_data):
            raise ValueError(f"Column '{y_column}' must be numeric for scatter plot")

        # Create and display plot
        result = plot_scatter_regression(x_data, y_data)

        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Scatter Plot:[/cyan] {x_column} vs {y_column}\n")
            console.print(result)
        else:
            print(f"\nScatter Plot: {x_column} vs {y_column}\n")
            print(result)

        return f"Plotted {x_column} vs {y_column} with regression"


class PlotHeatmapOperation(MathOperation):
    """Create a correlation heatmap of dataset."""

    name = "plot_heatmap"
    args = ["dataset"]
    help = "Plot correlation heatmap: plot_heatmap mydata"
    category = "visualization"

    @classmethod
    def execute(cls, dataset: str) -> str:
        """Create correlation heatmap of numeric columns.

        Args:
            dataset: Name of loaded dataset

        Returns:
            ASCII correlation heatmap
        """
        manager = get_data_manager()

        # Get dataset
        df = manager.get_dataset(dataset)

        # Get only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            raise ValueError(f"Dataset '{dataset}' has no numeric columns for correlation")

        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()

        # Create and display plot
        result = plot_heatmap(corr_matrix, labels=list(corr_matrix.columns))

        from utils.visual import console, preferences
        if preferences.colors_enabled:
            console.print(f"\n[cyan]Correlation Heatmap:[/cyan] {dataset}\n")
            console.print(result)
        else:
            print(f"\nCorrelation Heatmap: {dataset}\n")
            print(result)

        return f"Plotted correlation heatmap for {dataset}"

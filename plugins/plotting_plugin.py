"""Plotting operations plugin for Math CLI."""

from core.base_operations import MathOperation
from utils.plotting import plot_function_string, plot_expression, ASCIIPlotter


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

"""ASCII graph plotting utilities for Math CLI."""

import math
from typing import List, Callable, Tuple, Optional


class ASCIIPlotter:
    """Generate ASCII-based plots for functions and data."""

    def __init__(self, width: int = 60, height: int = 20):
        """Initialize the ASCII plotter.

        Args:
            width: Width of the plot in characters
            height: Height of the plot in characters
        """
        self.width = width
        self.height = height
        self.canvas = []
        self.x_min = 0
        self.x_max = 1
        self.y_min = 0
        self.y_max = 1

    def _init_canvas(self):
        """Initialize the plotting canvas."""
        self.canvas = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def _scale_x(self, x: float) -> int:
        """Scale x coordinate to canvas position.

        Args:
            x: Real x coordinate

        Returns:
            Canvas x position
        """
        if self.x_max == self.x_min:
            return self.width // 2
        scaled = (x - self.x_min) / (self.x_max - self.x_min) * (self.width - 1)
        return int(scaled)

    def _scale_y(self, y: float) -> int:
        """Scale y coordinate to canvas position.

        Args:
            y: Real y coordinate

        Returns:
            Canvas y position (inverted for display)
        """
        if self.y_max == self.y_min:
            return self.height // 2
        scaled = (y - self.y_min) / (self.y_max - self.y_min) * (self.height - 1)
        return self.height - 1 - int(scaled)

    def _set_pixel(self, x: int, y: int, char: str = '●'):
        """Set a pixel on the canvas.

        Args:
            x: Canvas x position
            y: Canvas y position
            char: Character to draw
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas[y][x] = char

    def _draw_axes(self):
        """Draw x and y axes."""
        # Find zero positions
        zero_x = self._scale_x(0)
        zero_y = self._scale_y(0)

        # Draw y-axis
        if 0 <= zero_x < self.width:
            for y in range(self.height):
                if self.canvas[y][zero_x] == ' ':
                    self.canvas[y][zero_x] = '│'

        # Draw x-axis
        if 0 <= zero_y < self.height:
            for x in range(self.width):
                if self.canvas[zero_y][x] == ' ':
                    self.canvas[zero_y][x] = '─'

        # Draw origin
        if 0 <= zero_x < self.width and 0 <= zero_y < self.height:
            self.canvas[zero_y][zero_x] = '┼'

    def _auto_scale(self, x_values: List[float], y_values: List[float]):
        """Automatically scale the plot based on data.

        Args:
            x_values: List of x coordinates
            y_values: List of y coordinates
        """
        if not x_values or not y_values:
            return

        self.x_min = min(x_values)
        self.x_max = max(x_values)
        self.y_min = min(y_values)
        self.y_max = max(y_values)

        # Add padding (10%)
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min

        if x_range > 0:
            padding_x = x_range * 0.1
            self.x_min -= padding_x
            self.x_max += padding_x

        if y_range > 0:
            padding_y = y_range * 0.1
            self.y_min -= padding_y
            self.y_max += padding_y

        # Handle constant values
        if x_range == 0:
            self.x_min -= 1
            self.x_max += 1
        if y_range == 0:
            self.y_min -= 1
            self.y_max += 1

    def plot_function(self, func: Callable[[float], float], x_start: float,
                     x_end: float, samples: int = 200, style: str = 'line') -> str:
        """Plot a mathematical function.

        Args:
            func: Function to plot (takes x, returns y)
            x_start: Start of x range
            x_end: End of x range
            samples: Number of sample points
            style: Plot style ('line', 'scatter', 'dots')

        Returns:
            ASCII art string of the plot
        """
        # Generate data points
        x_values = []
        y_values = []

        step = (x_end - x_start) / samples
        for i in range(samples + 1):
            x = x_start + i * step
            try:
                y = func(x)
                if math.isfinite(y):  # Skip inf and nan
                    x_values.append(x)
                    y_values.append(y)
            except (ValueError, ZeroDivisionError, OverflowError):
                # Skip invalid points
                pass

        if not x_values:
            return "Error: No valid points to plot"

        # Auto-scale
        self._auto_scale(x_values, y_values)

        # Initialize canvas
        self._init_canvas()

        # Draw axes
        self._draw_axes()

        # Plot points
        if style == 'line':
            self._plot_line(x_values, y_values)
        elif style == 'scatter':
            self._plot_scatter(x_values, y_values, '●')
        elif style == 'dots':
            self._plot_scatter(x_values, y_values, '·')
        else:
            self._plot_line(x_values, y_values)

        # Convert to string with labels
        return self._render_with_labels()

    def plot_data(self, y_values: List[float], x_values: Optional[List[float]] = None,
                  style: str = 'scatter') -> str:
        """Plot data points.

        Args:
            y_values: List of y coordinates
            x_values: Optional list of x coordinates (defaults to indices)
            style: Plot style ('scatter', 'line', 'bar')

        Returns:
            ASCII art string of the plot
        """
        if not y_values:
            return "Error: No data to plot"

        # Generate x values if not provided
        if x_values is None:
            x_values = list(range(1, len(y_values) + 1))

        if len(x_values) != len(y_values):
            return "Error: x and y must have the same length"

        # Auto-scale
        self._auto_scale(x_values, y_values)

        # Initialize canvas
        self._init_canvas()

        # Draw axes
        self._draw_axes()

        # Plot based on style
        if style == 'bar':
            self._plot_bars(x_values, y_values)
        elif style == 'line':
            self._plot_line(x_values, y_values)
        else:  # scatter
            self._plot_scatter(x_values, y_values, '●')

        # Convert to string with labels
        return self._render_with_labels()

    def _plot_line(self, x_values: List[float], y_values: List[float]):
        """Plot data as a connected line.

        Args:
            x_values: List of x coordinates
            y_values: List of y coordinates
        """
        prev_x = None
        prev_y = None

        for x, y in zip(x_values, y_values):
            canvas_x = self._scale_x(x)
            canvas_y = self._scale_y(y)

            if prev_x is not None:
                # Draw line between points
                self._draw_line(prev_x, prev_y, canvas_x, canvas_y)

            prev_x = canvas_x
            prev_y = canvas_y

    def _plot_scatter(self, x_values: List[float], y_values: List[float], char: str = '●'):
        """Plot data as scatter points.

        Args:
            x_values: List of x coordinates
            y_values: List of y coordinates
            char: Character to use for points
        """
        for x, y in zip(x_values, y_values):
            canvas_x = self._scale_x(x)
            canvas_y = self._scale_y(y)
            self._set_pixel(canvas_x, canvas_y, char)

    def _plot_bars(self, x_values: List[float], y_values: List[float]):
        """Plot data as vertical bars.

        Args:
            x_values: List of x coordinates
            y_values: List of y coordinates
        """
        zero_y = self._scale_y(0)

        for x, y in zip(x_values, y_values):
            canvas_x = self._scale_x(x)
            canvas_y = self._scale_y(y)

            # Draw vertical bar
            start_y = min(zero_y, canvas_y)
            end_y = max(zero_y, canvas_y)

            for y_pos in range(start_y, end_y + 1):
                if 0 <= y_pos < self.height:
                    self._set_pixel(canvas_x, y_pos, '█')

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int):
        """Draw a line between two points using Bresenham's algorithm.

        Args:
            x1, y1: Start point
            x2, y2: End point
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        x, y = x1, y1

        while True:
            # Choose character based on direction
            if dx > dy:
                char = '─'
            elif dy > dx:
                char = '│'
            else:
                char = '·'

            self._set_pixel(x, y, char)

            if x == x2 and y == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def _render_with_labels(self) -> str:
        """Render the canvas with axis labels.

        Returns:
            Complete plot as string with labels
        """
        lines = []

        # Format numbers for labels
        def fmt(val: float) -> str:
            if abs(val) >= 1000 or (abs(val) < 0.01 and val != 0):
                return f"{val:.1e}"
            elif abs(val) < 1:
                return f"{val:.3f}"
            else:
                return f"{val:.2f}"

        # Y-axis labels and canvas
        y_label_width = max(len(fmt(self.y_max)), len(fmt(self.y_min)), len(fmt(0))) + 1

        for i, row in enumerate(self.canvas):
            # Calculate y value for this row
            y_val = self.y_max - (i / (self.height - 1)) * (self.y_max - self.y_min)

            # Add y-axis label every few rows
            if i == 0:
                label = fmt(self.y_max)
            elif i == self.height - 1:
                label = fmt(self.y_min)
            elif i == self.height // 2:
                label = fmt((self.y_max + self.y_min) / 2)
            else:
                label = ""

            # Pad label
            label = label.rjust(y_label_width)
            lines.append(f"{label}│{''.join(row)}")

        # X-axis labels
        x_axis = " " * (y_label_width + 1) + "└" + "─" * self.width
        lines.append(x_axis)

        # X-axis values
        x_label_line = " " * (y_label_width + 2)
        x_label_line += fmt(self.x_min).ljust(self.width // 3)
        x_label_line += fmt((self.x_min + self.x_max) / 2).center(self.width // 3)
        x_label_line += fmt(self.x_max).rjust(self.width // 3)
        lines.append(x_label_line)

        return "\n".join(lines)


def plot_function_string(func_name: str, x_start: float, x_end: float,
                        width: int = 60, height: int = 20, style: str = 'line') -> str:
    """Plot a mathematical function by name.

    Args:
        func_name: Name of function (sin, cos, tan, exp, log, sqrt, etc.)
        x_start: Start of x range
        x_end: End of x range
        width: Plot width
        height: Plot height
        style: Plot style

    Returns:
        ASCII art plot
    """
    # Map function names to implementations
    functions = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': lambda x: math.sqrt(x) if x >= 0 else float('nan'),
        'abs': abs,
        'square': lambda x: x ** 2,
        'cube': lambda x: x ** 3,
        'inv': lambda x: 1 / x if x != 0 else float('nan'),
    }

    if func_name not in functions:
        return f"Error: Unknown function '{func_name}'"

    plotter = ASCIIPlotter(width=width, height=height)
    return plotter.plot_function(functions[func_name], x_start, x_end, style=style)


def plot_expression(expression: str, x_start: float, x_end: float,
                   width: int = 60, height: int = 20) -> str:
    """Plot a mathematical expression.

    Args:
        expression: Expression string with 'x' as variable
        x_start: Start of x range
        x_end: End of x range
        width: Plot width
        height: Plot height

    Returns:
        ASCII art plot or error message
    """
    # Create a safe evaluation function
    safe_dict = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'abs': abs,
        'pi': math.pi,
        'e': math.e,
        '__builtins__': {}  # Prevent access to builtins
    }

    try:
        # Test evaluation
        test_func = lambda x: eval(expression, {"x": x, **safe_dict})
        test_func(0)  # Test that it works

        plotter = ASCIIPlotter(width=width, height=height)
        return plotter.plot_function(test_func, x_start, x_end)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

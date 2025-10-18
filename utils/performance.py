"""Performance profiling and optimization utilities for Math CLI."""

import time
import functools
import psutil
import os
from typing import Callable, Any, Dict, Optional
from contextlib import contextmanager


class PerformanceMonitor:
    """Monitor and track performance metrics."""

    def __init__(self):
        """Initialize the performance monitor."""
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.process = psutil.Process(os.getpid())
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

    def record_metric(self, name: str, duration: float, memory_delta: float = 0):
        """Record a performance metric.

        Args:
            name: Name of the operation
            duration: Duration in seconds
            memory_delta: Memory change in MB
        """
        if name not in self.metrics:
            self.metrics[name] = {
                'count': 0,
                'total_time': 0,
                'total_memory': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'avg_time': 0
            }

        metrics = self.metrics[name]
        metrics['count'] += 1
        metrics['total_time'] += duration
        metrics['total_memory'] += memory_delta
        metrics['min_time'] = min(metrics['min_time'], duration)
        metrics['max_time'] = max(metrics['max_time'], duration)
        metrics['avg_time'] = metrics['total_time'] / metrics['count']

    def get_metrics(self, name: Optional[str] = None) -> Dict:
        """Get performance metrics.

        Args:
            name: Optional specific metric name

        Returns:
            Dictionary of metrics
        """
        if name:
            return self.metrics.get(name, {})
        return self.metrics.copy()

    def get_current_memory(self) -> float:
        """Get current memory usage in MB.

        Returns:
            Memory usage in megabytes
        """
        return self.process.memory_info().rss / 1024 / 1024

    def get_memory_delta(self) -> float:
        """Get memory delta since start in MB.

        Returns:
            Memory change in megabytes
        """
        return self.get_current_memory() - self.start_memory

    def get_uptime(self) -> float:
        """Get application uptime in seconds.

        Returns:
            Uptime in seconds
        """
        return time.time() - self.start_time

    def print_summary(self):
        """Print a summary of performance metrics."""
        from utils.visual import console, preferences

        if not self.metrics:
            print("No performance metrics recorded")
            return

        if preferences.colors_enabled:
            from rich.table import Table
            from rich import box

            table = Table(
                title="Performance Metrics",
                box=box.ROUNDED,
                show_header=True
            )
            table.add_column("Operation", style="cyan")
            table.add_column("Count", style="yellow", justify="right")
            table.add_column("Avg Time", style="green", justify="right")
            table.add_column("Min Time", style="dim", justify="right")
            table.add_column("Max Time", style="dim", justify="right")
            table.add_column("Total Time", style="magenta", justify="right")

            for name, metrics in sorted(self.metrics.items()):
                table.add_row(
                    name,
                    str(metrics['count']),
                    f"{metrics['avg_time']*1000:.2f}ms",
                    f"{metrics['min_time']*1000:.2f}ms",
                    f"{metrics['max_time']*1000:.2f}ms",
                    f"{metrics['total_time']*1000:.2f}ms"
                )

            console.print(table)

            # System metrics
            console.print(f"\n[cyan]Memory Usage:[/cyan] {self.get_current_memory():.2f} MB")
            console.print(f"[cyan]Memory Delta:[/cyan] {self.get_memory_delta():.2f} MB")
            console.print(f"[cyan]Uptime:[/cyan] {self.get_uptime():.2f}s")
        else:
            print("\nPerformance Metrics:")
            print("-" * 80)
            for name, metrics in sorted(self.metrics.items()):
                print(f"{name}:")
                print(f"  Count: {metrics['count']}")
                print(f"  Avg Time: {metrics['avg_time']*1000:.2f}ms")
                print(f"  Min Time: {metrics['min_time']*1000:.2f}ms")
                print(f"  Max Time: {metrics['max_time']*1000:.2f}ms")
                print(f"  Total Time: {metrics['total_time']*1000:.2f}ms")
            print(f"\nMemory Usage: {self.get_current_memory():.2f} MB")
            print(f"Memory Delta: {self.get_memory_delta():.2f} MB")
            print(f"Uptime: {self.get_uptime():.2f}s")

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.start_time = time.time()
        self.start_memory = self.get_current_memory()


# Global performance monitor instance
_monitor = None


def get_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance.

    Returns:
        PerformanceMonitor instance
    """
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor


def profile(name: Optional[str] = None, track_memory: bool = False):
    """Decorator to profile function execution time.

    Args:
        name: Optional custom name for the metric
        track_memory: Whether to track memory usage

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        metric_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor = get_monitor()
            start_time = time.time()
            start_memory = monitor.get_current_memory() if track_memory else 0

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                memory_delta = (monitor.get_current_memory() - start_memory) if track_memory else 0
                monitor.record_metric(metric_name, duration, memory_delta)

        return wrapper
    return decorator


@contextmanager
def measure(name: str, track_memory: bool = False):
    """Context manager to measure execution time.

    Args:
        name: Name of the operation
        track_memory: Whether to track memory usage

    Example:
        with measure("calculation"):
            result = complex_operation()
    """
    monitor = get_monitor()
    start_time = time.time()
    start_memory = monitor.get_current_memory() if track_memory else 0

    try:
        yield
    finally:
        duration = time.time() - start_time
        memory_delta = (monitor.get_current_memory() - start_memory) if track_memory else 0
        monitor.record_metric(name, duration, memory_delta)


def benchmark(func: Callable, iterations: int = 100, *args, **kwargs) -> Dict[str, float]:
    """Benchmark a function by running it multiple times.

    Args:
        func: Function to benchmark
        iterations: Number of iterations
        *args: Arguments to pass to function
        **kwargs: Keyword arguments to pass to function

    Returns:
        Dictionary with benchmark results
    """
    times = []

    # Warmup
    for _ in range(min(10, iterations // 10)):
        func(*args, **kwargs)

    # Actual benchmark
    for _ in range(iterations):
        start = time.time()
        func(*args, **kwargs)
        times.append(time.time() - start)

    return {
        'min': min(times) * 1000,  # ms
        'max': max(times) * 1000,  # ms
        'avg': sum(times) / len(times) * 1000,  # ms
        'total': sum(times) * 1000,  # ms
        'iterations': iterations
    }


def get_startup_metrics() -> Dict[str, Any]:
    """Get application startup performance metrics.

    Returns:
        Dictionary with startup metrics
    """
    monitor = get_monitor()
    return {
        'uptime': monitor.get_uptime(),
        'memory_usage': monitor.get_current_memory(),
        'memory_delta': monitor.get_memory_delta()
    }


class PerformanceWarning:
    """Track and warn about performance issues."""

    def __init__(self, threshold_ms: float = 100):
        """Initialize performance warning tracker.

        Args:
            threshold_ms: Threshold in milliseconds for warnings
        """
        self.threshold = threshold_ms / 1000  # Convert to seconds
        self.warnings = []

    def check(self, name: str, duration: float):
        """Check if duration exceeds threshold.

        Args:
            name: Operation name
            duration: Duration in seconds
        """
        if duration > self.threshold:
            warning = {
                'name': name,
                'duration': duration * 1000,  # ms
                'threshold': self.threshold * 1000,  # ms
                'excess': (duration - self.threshold) * 1000  # ms
            }
            self.warnings.append(warning)

            # Print warning if visual system available
            try:
                from utils.visual import print_warning
                print_warning(
                    f"Performance: {name} took {duration*1000:.2f}ms "
                    f"(threshold: {self.threshold*1000:.2f}ms)"
                )
            except ImportError:
                pass

    def get_warnings(self):
        """Get all performance warnings.

        Returns:
            List of warning dictionaries
        """
        return self.warnings.copy()

    def clear(self):
        """Clear all warnings."""
        self.warnings.clear()

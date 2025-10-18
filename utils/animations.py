"""Advanced animations and visual polish for Math CLI."""

import time
import math
from typing import Optional, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box
from rich.panel import Panel


class MilestoneDetector:
    """Detect and celebrate calculation milestones."""

    def __init__(self):
        """Initialize milestone detector."""
        self.calculation_count = 0
        self.milestones = [10, 50, 100, 250, 500, 1000]

    def increment(self) -> Optional[int]:
        """Increment calculation count and check for milestones.

        Returns:
            Milestone number if reached, None otherwise
        """
        self.calculation_count += 1
        if self.calculation_count in self.milestones:
            return self.calculation_count
        return None

    def get_count(self) -> int:
        """Get current calculation count."""
        return self.calculation_count

    def reset(self):
        """Reset calculation count."""
        self.calculation_count = 0


class SpecialNumberDetector:
    """Detect special mathematical numbers and constants."""

    def __init__(self):
        """Initialize special number detector."""
        self.special_numbers = {
            'pi': (math.pi, 0.0001, '🥧'),
            'e': (math.e, 0.0001, '📈'),
            'phi': ((1 + math.sqrt(5)) / 2, 0.0001, '✨'),  # Golden ratio
            'sqrt2': (math.sqrt(2), 0.0001, '√'),
            'euler_gamma': (0.5772156649, 0.0001, 'γ'),  # Euler-Mascheroni constant
        }

    def check_number(self, value: float) -> Optional[Tuple[str, str]]:
        """Check if a number is special.

        Args:
            value: Number to check

        Returns:
            Tuple of (name, emoji) if special, None otherwise
        """
        # Check for infinity
        if value == float('inf'):
            return ('infinity', '∞')
        if value == float('-inf'):
            return ('negative infinity', '-∞')

        # Check for zero
        if abs(value) < 1e-10:
            return ('zero', '0️⃣')

        # Check for one
        if abs(value - 1.0) < 1e-10:
            return ('one', '1️⃣')

        # Check special constants
        for name, (const_value, tolerance, emoji) in self.special_numbers.items():
            if abs(value - const_value) < tolerance:
                return (name, emoji)

        # Check if perfect square
        if value > 0 and value == int(value):
            sqrt_val = math.sqrt(value)
            if abs(sqrt_val - round(sqrt_val)) < 1e-10:
                return ('perfect square', '²')

        # Check if Fibonacci number
        if self._is_fibonacci(value):
            return ('Fibonacci number', '🐚')

        # Check if power of 2
        if value > 0 and value == int(value):
            log2_val = math.log2(value)
            if abs(log2_val - round(log2_val)) < 1e-10:
                return ('power of 2', '💪')

        return None

    def _is_fibonacci(self, n: float) -> bool:
        """Check if number is a Fibonacci number.

        Args:
            n: Number to check

        Returns:
            True if Fibonacci number
        """
        if n != int(n) or n < 0:
            return False

        n = int(n)

        # A number is Fibonacci if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
        def is_perfect_square(x):
            s = int(math.sqrt(x))
            return s * s == x

        return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)


class AnimationController:
    """Control animations and visual effects."""

    def __init__(self, console: Console, animations_enabled: bool = True):
        """Initialize animation controller.

        Args:
            console: Rich console instance
            animations_enabled: Whether animations are enabled
        """
        self.console = console
        self.animations_enabled = animations_enabled

    def celebrate_milestone(self, milestone: int):
        """Display celebration animation for milestone.

        Args:
            milestone: Milestone number reached
        """
        if not self.animations_enabled:
            self.console.print(f"\n🎉 Milestone reached: {milestone} calculations!")
            return

        # Create celebration message
        messages = {
            10: "You're getting the hang of it!",
            50: "Math wizard in training!",
            100: "Century of calculations!",
            250: "Quarter-thousand milestone!",
            500: "Half a millennium of math!",
            1000: "Mathematical mastery achieved!",
        }

        message = messages.get(milestone, f"{milestone} calculations!")

        # Animated celebration
        self.console.print()
        for _ in range(3):
            self.console.print("🎉 " * 10, style="bold yellow", end="\r")
            time.sleep(0.15)
            self.console.print("   " * 10, end="\r")
            time.sleep(0.15)

        # Final message
        panel = Panel(
            Text(f"🎊 {message} 🎊", justify="center", style="bold magenta"),
            box=box.DOUBLE,
            border_style="yellow",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()

    def show_special_number(self, name: str, emoji: str, value: float):
        """Display animation for special number detection.

        Args:
            name: Name of special number
            emoji: Emoji for the number
            value: The value
        """
        if not self.animations_enabled:
            self.console.print(f"\n✨ Special number detected: {name} {emoji}")
            return

        # Special number messages
        messages = {
            'pi': "The circle constant!",
            'e': "The natural constant!",
            'phi': "The golden ratio!",
            'zero': "The origin of all numbers!",
            'one': "The multiplicative identity!",
            'perfect square': "A perfect square!",
            'Fibonacci number': "From the Fibonacci sequence!",
            'power of 2': "A power of two!",
            'infinity': "To infinity and beyond!",
        }

        message = messages.get(name, f"The {name}!")

        # Animated reveal
        self.console.print()
        text = Text()
        text.append("✨ ", style="yellow")
        text.append(f"{emoji} ", style="bold cyan")
        text.append(message, style="bold white")
        text.append(f" {emoji}", style="bold cyan")
        text.append(" ✨", style="yellow")

        panel = Panel(
            text,
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2)
        )

        # Blink effect
        for _ in range(2):
            self.console.print(panel)
            time.sleep(0.3)
            # Move cursor up to overwrite
            self.console.print("\033[F" * 3, end="")
            time.sleep(0.2)

        self.console.print(panel)
        self.console.print()

    def loading_animation(self, message: str = "Processing", duration: float = 1.0):
        """Show a loading animation.

        Args:
            message: Loading message
            duration: How long to show animation
        """
        if not self.animations_enabled:
            self.console.print(f"{message}...")
            return

        with Progress(
            SpinnerColumn("dots"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(f"[cyan]{message}...", total=None)
            time.sleep(duration)
            progress.remove_task(task)

    def smooth_result_reveal(self, result: str, color: str = "green"):
        """Smoothly reveal a result.

        Args:
            result: Result to display
            color: Color for the result
        """
        if not self.animations_enabled:
            self.console.print(f"Result: {result}", style=color)
            return

        # Character-by-character reveal
        self.console.print("Result: ", style="white", end="")
        for char in str(result):
            self.console.print(char, style=f"bold {color}", end="")
            time.sleep(0.02)
        self.console.print()

    def easter_egg_pi_day(self):
        """Display Pi Day easter egg."""
        if not self.animations_enabled:
            self.console.print("\n🥧 Happy Pi Day! 3.14159...")
            return

        pi_ascii = """
        ╔═══════════════════════════╗
        ║     HAPPY PI DAY! 🥧      ║
        ║                           ║
        ║   π = 3.14159265358979... ║
        ║                           ║
        ║   "Pi is exactly 3!"      ║
        ║        - Engineers         ║
        ╚═══════════════════════════╝
        """

        self.console.print(pi_ascii, style="bold cyan")

    def easter_egg_euler(self):
        """Display Euler's identity easter egg."""
        if not self.animations_enabled:
            self.console.print("\n📐 Euler's Identity: e^(iπ) + 1 = 0")
            return

        euler_ascii = """
        ╔═════════════════════════════════╗
        ║   EULER'S IDENTITY 🎭          ║
        ║                                 ║
        ║     e^(iπ) + 1 = 0             ║
        ║                                 ║
        ║  "The most beautiful equation"  ║
        ╚═════════════════════════════════╝
        """

        self.console.print(euler_ascii, style="bold magenta")

    def easter_egg_golden_ratio(self):
        """Display Golden Ratio easter egg."""
        if not self.animations_enabled:
            self.console.print("\n✨ Golden Ratio: φ = 1.618...")
            return

        golden_ascii = """
        ╔═════════════════════════════════╗
        ║   THE GOLDEN RATIO ✨           ║
        ║                                 ║
        ║     φ = (1 + √5) / 2           ║
        ║     φ ≈ 1.618033988749...      ║
        ║                                 ║
        ║  Nature's most perfect number   ║
        ╚═════════════════════════════════╝
        """

        self.console.print(golden_ascii, style="bold yellow")

    def easter_egg_42(self):
        """Display '42' easter egg (Hitchhiker's Guide reference)."""
        if not self.animations_enabled:
            self.console.print("\n🌌 42: The Answer to Life, the Universe, and Everything!")
            return

        fortytwo_ascii = """
        ╔═══════════════════════════════════════╗
        ║   THE ANSWER TO EVERYTHING 🌌         ║
        ║                                       ║
        ║              42                       ║
        ║                                       ║
        ║  "Life, the Universe, and Everything" ║
        ║     - The Hitchhiker's Guide          ║
        ╚═══════════════════════════════════════╝
        """

        self.console.print(fortytwo_ascii, style="bold blue")

    def check_and_show_easter_egg(self, value: float):
        """Check for and display easter eggs.

        Args:
            value: Result value to check
        """
        # Check for 42
        if abs(value - 42.0) < 1e-10:
            self.easter_egg_42()
            return True

        # Check for pi
        if abs(value - math.pi) < 0.0001:
            self.easter_egg_pi_day()
            return True

        # Check for e
        if abs(value - math.e) < 0.0001:
            self.easter_egg_euler()
            return True

        # Check for golden ratio
        phi = (1 + math.sqrt(5)) / 2
        if abs(value - phi) < 0.0001:
            self.easter_egg_golden_ratio()
            return True

        return False


class TransitionEffects:
    """Smooth transition effects."""

    def __init__(self, console: Console, animations_enabled: bool = True):
        """Initialize transition effects.

        Args:
            console: Rich console instance
            animations_enabled: Whether animations are enabled
        """
        self.console = console
        self.animations_enabled = animations_enabled

    def fade_in_text(self, text: str, style: str = "white"):
        """Fade in text effect.

        Args:
            text: Text to display
            style: Text style
        """
        if not self.animations_enabled:
            self.console.print(text, style=style)
            return

        # Simulate fade by gradually increasing brightness
        styles = ["dim", "white", f"bold {style}"]
        for s in styles:
            self.console.print(text, style=s, end="\r")
            time.sleep(0.1)
        self.console.print(text, style=f"bold {style}")

    def slide_in_panel(self, title: str, content: str, style: str = "cyan"):
        """Slide in a panel from the left.

        Args:
            title: Panel title
            content: Panel content
            style: Border style
        """
        if not self.animations_enabled:
            panel = Panel(content, title=title, border_style=style)
            self.console.print(panel)
            return

        # Create panel
        panel = Panel(content, title=title, border_style=style, padding=(1, 2))

        # Simple appearance with brief pause
        time.sleep(0.1)
        self.console.print(panel)

    def pulsing_text(self, text: str, pulses: int = 3):
        """Create pulsing text effect.

        Args:
            text: Text to pulse
            pulses: Number of pulses
        """
        if not self.animations_enabled:
            self.console.print(text)
            return

        for _ in range(pulses):
            self.console.print(text, style="bold white", end="\r")
            time.sleep(0.3)
            self.console.print(text, style="dim white", end="\r")
            time.sleep(0.3)
        self.console.print(text, style="bold white")


# Global instances
_milestone_detector = None
_special_number_detector = None


def get_milestone_detector() -> MilestoneDetector:
    """Get global milestone detector instance.

    Returns:
        MilestoneDetector instance
    """
    global _milestone_detector
    if _milestone_detector is None:
        _milestone_detector = MilestoneDetector()
    return _milestone_detector


def get_special_number_detector() -> SpecialNumberDetector:
    """Get global special number detector instance.

    Returns:
        SpecialNumberDetector instance
    """
    global _special_number_detector
    if _special_number_detector is None:
        _special_number_detector = SpecialNumberDetector()
    return _special_number_detector

"""Accessibility utilities for Math CLI to ensure WCAG 2.1 AA compliance."""

from typing import Dict, Optional, Tuple
import re


class AccessibilityManager:
    """Manage accessibility settings and features."""

    def __init__(self):
        """Initialize the accessibility manager."""
        self.settings = {
            'screen_reader_mode': False,
            'high_contrast': False,
            'reduce_motion': False,
            'keyboard_only': False,
            'large_text': False,
            'audio_cues': False,
            'verbose_output': False,
        }

    def enable_screen_reader_mode(self):
        """Enable screen reader friendly mode."""
        self.settings['screen_reader_mode'] = True
        self.settings['reduce_motion'] = True  # Auto-enable
        self.settings['verbose_output'] = True  # Auto-enable

    def enable_high_contrast(self):
        """Enable high contrast mode."""
        self.settings['high_contrast'] = True

    def enable_reduced_motion(self):
        """Enable reduced motion mode."""
        self.settings['reduce_motion'] = True

    def is_screen_reader_mode(self) -> bool:
        """Check if screen reader mode is enabled."""
        return self.settings['screen_reader_mode']

    def is_high_contrast(self) -> bool:
        """Check if high contrast mode is enabled."""
        return self.settings['high_contrast']

    def should_reduce_motion(self) -> bool:
        """Check if motion should be reduced."""
        return self.settings['reduce_motion']

    def get_setting(self, key: str) -> bool:
        """Get an accessibility setting."""
        return self.settings.get(key, False)

    def set_setting(self, key: str, value: bool):
        """Set an accessibility setting."""
        if key in self.settings:
            self.settings[key] = value

    def get_all_settings(self) -> Dict[str, bool]:
        """Get all accessibility settings."""
        return self.settings.copy()


class ColorContrastChecker:
    """Check color contrast ratios for WCAG compliance."""

    def __init__(self):
        """Initialize the contrast checker."""
        # Standard terminal color RGB values (approximate)
        self.colors = {
            'black': (0, 0, 0),
            'red': (205, 0, 0),
            'green': (0, 205, 0),
            'yellow': (205, 205, 0),
            'blue': (0, 0, 238),
            'magenta': (205, 0, 205),
            'cyan': (0, 205, 205),
            'white': (229, 229, 229),
            'bright_black': (127, 127, 127),
            'bright_red': (255, 0, 0),
            'bright_green': (0, 255, 0),
            'bright_yellow': (255, 255, 0),
            'bright_blue': (92, 92, 255),
            'bright_magenta': (255, 0, 255),
            'bright_cyan': (0, 255, 255),
            'bright_white': (255, 255, 255),
        }

    def _relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance of RGB color.

        Args:
            rgb: RGB tuple (0-255 range)

        Returns:
            Relative luminance (0-1 range)
        """
        # Convert to 0-1 range
        r, g, b = [x / 255.0 for x in rgb]

        # Apply gamma correction
        def gamma(c):
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = gamma(r), gamma(g), gamma(b)

        # Calculate luminance
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors.

        Args:
            color1: First color name
            color2: Second color name

        Returns:
            Contrast ratio (1-21 range)
        """
        rgb1 = self.colors.get(color1, self.colors['white'])
        rgb2 = self.colors.get(color2, self.colors['black'])

        l1 = self._relative_luminance(rgb1)
        l2 = self._relative_luminance(rgb2)

        # Ensure l1 is lighter
        if l2 > l1:
            l1, l2 = l2, l1

        return (l1 + 0.05) / (l2 + 0.05)

    def meets_wcag_aa(self, color1: str, color2: str, text_size: str = 'normal') -> bool:
        """Check if color combination meets WCAG AA standards.

        Args:
            color1: Foreground color
            color2: Background color
            text_size: 'normal' or 'large'

        Returns:
            True if meets WCAG AA
        """
        ratio = self.contrast_ratio(color1, color2)

        if text_size == 'large':
            return ratio >= 3.0  # WCAG AA for large text
        else:
            return ratio >= 4.5  # WCAG AA for normal text

    def meets_wcag_aaa(self, color1: str, color2: str, text_size: str = 'normal') -> bool:
        """Check if color combination meets WCAG AAA standards.

        Args:
            color1: Foreground color
            color2: Background color
            text_size: 'normal' or 'large'

        Returns:
            True if meets WCAG AAA
        """
        ratio = self.contrast_ratio(color1, color2)

        if text_size == 'large':
            return ratio >= 4.5  # WCAG AAA for large text
        else:
            return ratio >= 7.0  # WCAG AAA for normal text


class ScreenReaderFormatter:
    """Format output for screen readers."""

    def __init__(self):
        """Initialize the formatter."""
        pass

    def format_result(self, operation: str, result: float) -> str:
        """Format a calculation result for screen readers.

        Args:
            operation: The operation performed
            result: The result value

        Returns:
            Screen reader friendly description
        """
        # Remove formatting and make verbose
        text = f"Operation: {operation}. Result: {self._speak_number(result)}"
        return text

    def format_error(self, error_msg: str) -> str:
        """Format an error message for screen readers.

        Args:
            error_msg: The error message

        Returns:
            Screen reader friendly error
        """
        return f"Error encountered. {error_msg}"

    def format_help(self, operation: str, description: str) -> str:
        """Format help text for screen readers.

        Args:
            operation: Operation name
            description: Operation description

        Returns:
            Screen reader friendly help
        """
        return f"{operation} operation. {description}"

    def _speak_number(self, num: float) -> str:
        """Convert a number to speakable text.

        Args:
            num: Number to convert

        Returns:
            Speakable representation
        """
        # Handle special values
        if num == float('inf'):
            return "infinity"
        elif num == float('-inf'):
            return "negative infinity"
        elif num != num:  # NaN
            return "not a number"

        # Format regular numbers
        if isinstance(num, int) or num.is_integer():
            return str(int(num))

        # For decimals, be more explicit
        if abs(num) < 0.01:
            return f"{num:.6e}".replace('e', ' times 10 to the power ')
        else:
            return f"{num:.4f}"

    def remove_formatting(self, text: str) -> str:
        """Remove visual formatting for screen readers.

        Args:
            text: Formatted text

        Returns:
            Plain text without formatting
        """
        # Remove Rich markup
        text = re.sub(r'\[.*?\]', '', text)
        # Remove ANSI codes
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        # Remove box drawing characters
        text = text.replace('│', '|').replace('─', '-')
        text = text.replace('╭', '+').replace('╮', '+')
        text = text.replace('╰', '+').replace('╯', '+')
        text = text.replace('├', '+').replace('┤', '+')
        text = text.replace('┬', '+').replace('┴', '+')
        text = text.replace('┼', '+')
        # Remove emoji
        text = re.sub(r'[^\x00-\x7F]+', '', text)

        return text.strip()


def check_terminal_accessibility() -> Dict[str, bool]:
    """Check terminal accessibility features.

    Returns:
        Dictionary of available accessibility features
    """
    import os
    import sys

    features = {
        'colors_supported': True,
        'unicode_supported': True,
        'terminal_detected': sys.stdout.isatty(),
        'screen_reader_detected': False,
    }

    # Check for common screen reader environment variables
    screen_reader_vars = ['NVDA', 'JAWS', 'NARRATOR', 'VOICEOVER']
    for var in screen_reader_vars:
        if os.environ.get(var):
            features['screen_reader_detected'] = True
            break

    # Check for reduced motion preference
    if os.environ.get('REDUCE_MOTION') or os.environ.get('PREFERS_REDUCED_MOTION'):
        features['reduce_motion_preferred'] = True

    # Check terminal capabilities
    try:
        import curses
        curses.setupterm()
        features['colors_supported'] = curses.tigetnum('colors') > 0
    except:
        pass

    return features


class KeyboardNavigationHelper:
    """Helper for keyboard-only navigation."""

    def __init__(self):
        """Initialize keyboard navigation helper."""
        self.shortcuts = {
            'Ctrl+L': 'Clear screen',
            'Ctrl+D': 'Exit application',
            'Ctrl+C': 'Cancel current input',
            'Tab': 'Autocomplete operation',
            '↑': 'Previous command in history',
            '↓': 'Next command in history',
            'Enter': 'Execute command',
            'Esc': 'Cancel multiline input',
        }

    def get_shortcuts(self) -> Dict[str, str]:
        """Get all keyboard shortcuts.

        Returns:
            Dictionary of shortcuts and their descriptions
        """
        return self.shortcuts.copy()

    def describe_shortcuts(self) -> str:
        """Get a description of all shortcuts.

        Returns:
            Human-readable shortcuts description
        """
        lines = ["Keyboard Shortcuts:"]
        for key, desc in self.shortcuts.items():
            lines.append(f"  {key}: {desc}")
        return '\n'.join(lines)


# Global accessibility manager instance
_accessibility_manager = None


def get_accessibility_manager() -> AccessibilityManager:
    """Get the global accessibility manager instance.

    Returns:
        AccessibilityManager instance
    """
    global _accessibility_manager
    if _accessibility_manager is None:
        _accessibility_manager = AccessibilityManager()
    return _accessibility_manager

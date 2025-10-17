"""Theme system for Math CLI with multiple color schemes."""

from typing import Dict, Any


class Theme:
    """Base theme class defining color schemes."""

    def __init__(self, name: str, colors: Dict[str, str], description: str = ""):
        """Initialize a theme.

        Args:
            name: Theme name identifier
            colors: Dictionary mapping color keys to rich color styles
            description: Human-readable theme description
        """
        self.name = name
        self.colors = colors
        self.description = description

    def get_color(self, key: str, default: str = "white") -> str:
        """Get a color value for a given key.

        Args:
            key: Color key to retrieve
            default: Default color if key not found

        Returns:
            Color style string
        """
        return self.colors.get(key, default)


# Define available themes

DEFAULT_THEME = Theme(
    name="default",
    description="Standard vibrant color scheme for Math CLI",
    colors={
        'input': 'cyan',
        'output': 'green bold',
        'error': 'red bold',
        'warning': 'yellow',
        'info': 'blue',
        'success': 'green',
        'operator': 'magenta',
        'number': 'cyan',
        'command': 'yellow bold',
        'help': 'blue',
        'prompt': 'white',
        'dim': 'dim',
        'highlight': 'bright_cyan bold',
        'banner_primary': 'bright_cyan bold',
        'banner_secondary': 'cyan',
        'banner_title': 'bright_yellow bold',
        'table_header': 'bold cyan',
        'table_border': 'cyan',
    }
)

DARK_THEME = Theme(
    name="dark",
    description="Darker color scheme optimized for dark terminals",
    colors={
        'input': 'bright_blue',
        'output': 'bright_green bold',
        'error': 'bright_red bold',
        'warning': 'bright_yellow',
        'info': 'bright_blue',
        'success': 'bright_green',
        'operator': 'bright_magenta',
        'number': 'bright_cyan',
        'command': 'bright_yellow bold',
        'help': 'bright_blue',
        'prompt': 'bright_white',
        'dim': 'bright_black',
        'highlight': 'bright_cyan bold',
        'banner_primary': 'bright_white bold',
        'banner_secondary': 'bright_blue',
        'banner_title': 'bright_yellow bold',
        'table_header': 'bold bright_blue',
        'table_border': 'bright_blue',
    }
)

LIGHT_THEME = Theme(
    name="light",
    description="Light color scheme optimized for light terminals",
    colors={
        'input': 'blue',
        'output': 'green bold',
        'error': 'red bold',
        'warning': 'yellow',
        'info': 'blue',
        'success': 'green',
        'operator': 'magenta',
        'number': 'blue',
        'command': 'yellow bold',
        'help': 'blue',
        'prompt': 'black',
        'dim': 'bright_black',
        'highlight': 'blue bold',
        'banner_primary': 'blue bold',
        'banner_secondary': 'blue',
        'banner_title': 'yellow bold',
        'table_header': 'bold blue',
        'table_border': 'blue',
    }
)

HIGH_CONTRAST_THEME = Theme(
    name="high-contrast",
    description="High contrast theme for accessibility",
    colors={
        'input': 'bright_white',
        'output': 'bright_green bold',
        'error': 'bright_red bold',
        'warning': 'bright_yellow bold',
        'info': 'bright_white',
        'success': 'bright_green bold',
        'operator': 'bright_white',
        'number': 'bright_white bold',
        'command': 'bright_white bold',
        'help': 'bright_white',
        'prompt': 'bright_white',
        'dim': 'white',
        'highlight': 'bright_white bold',
        'banner_primary': 'bright_white bold',
        'banner_secondary': 'bright_white',
        'banner_title': 'bright_white bold',
        'table_header': 'bold bright_white',
        'table_border': 'bright_white',
    }
)

OCEAN_THEME = Theme(
    name="ocean",
    description="Calming ocean-inspired blue and teal theme",
    colors={
        'input': 'bright_cyan',
        'output': 'cyan bold',
        'error': 'red bold',
        'warning': 'yellow',
        'info': 'blue',
        'success': 'cyan',
        'operator': 'bright_blue',
        'number': 'bright_cyan',
        'command': 'cyan bold',
        'help': 'blue',
        'prompt': 'bright_white',
        'dim': 'dim',
        'highlight': 'bright_cyan bold',
        'banner_primary': 'bright_cyan bold',
        'banner_secondary': 'blue',
        'banner_title': 'bright_white bold',
        'table_header': 'bold bright_cyan',
        'table_border': 'cyan',
    }
)

FOREST_THEME = Theme(
    name="forest",
    description="Nature-inspired green theme",
    colors={
        'input': 'bright_green',
        'output': 'green bold',
        'error': 'red bold',
        'warning': 'yellow',
        'info': 'green',
        'success': 'bright_green',
        'operator': 'yellow',
        'number': 'bright_green',
        'command': 'bright_green bold',
        'help': 'green',
        'prompt': 'bright_white',
        'dim': 'dim',
        'highlight': 'bright_green bold',
        'banner_primary': 'bright_green bold',
        'banner_secondary': 'green',
        'banner_title': 'bright_yellow bold',
        'table_header': 'bold bright_green',
        'table_border': 'green',
    }
)

SUNSET_THEME = Theme(
    name="sunset",
    description="Warm sunset colors with orange and purple tones",
    colors={
        'input': 'bright_yellow',
        'output': 'yellow bold',
        'error': 'red bold',
        'warning': 'bright_yellow',
        'info': 'magenta',
        'success': 'yellow',
        'operator': 'bright_magenta',
        'number': 'bright_yellow',
        'command': 'bright_yellow bold',
        'help': 'magenta',
        'prompt': 'bright_white',
        'dim': 'dim',
        'highlight': 'bright_yellow bold',
        'banner_primary': 'bright_magenta bold',
        'banner_secondary': 'magenta',
        'banner_title': 'bright_yellow bold',
        'table_header': 'bold bright_yellow',
        'table_border': 'yellow',
    }
)

MONOCHROME_THEME = Theme(
    name="monochrome",
    description="Classic monochrome theme with shades of gray",
    colors={
        'input': 'white',
        'output': 'bright_white bold',
        'error': 'bright_white bold',
        'warning': 'white',
        'info': 'white',
        'success': 'bright_white',
        'operator': 'white',
        'number': 'bright_white',
        'command': 'bright_white bold',
        'help': 'white',
        'prompt': 'white',
        'dim': 'dim',
        'highlight': 'bright_white bold',
        'banner_primary': 'bright_white bold',
        'banner_secondary': 'white',
        'banner_title': 'bright_white bold',
        'table_header': 'bold bright_white',
        'table_border': 'white',
    }
)


# Theme registry
THEMES: Dict[str, Theme] = {
    'default': DEFAULT_THEME,
    'dark': DARK_THEME,
    'light': LIGHT_THEME,
    'high-contrast': HIGH_CONTRAST_THEME,
    'ocean': OCEAN_THEME,
    'forest': FOREST_THEME,
    'sunset': SUNSET_THEME,
    'monochrome': MONOCHROME_THEME,
}


class ThemeManager:
    """Manage theme selection and application."""

    def __init__(self, theme_name: str = "default"):
        """Initialize the theme manager.

        Args:
            theme_name: Name of the theme to load
        """
        self.current_theme = self.get_theme(theme_name)

    def get_theme(self, theme_name: str) -> Theme:
        """Get a theme by name.

        Args:
            theme_name: Theme name to retrieve

        Returns:
            Theme object (defaults to DEFAULT_THEME if not found)
        """
        return THEMES.get(theme_name, DEFAULT_THEME)

    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme.

        Args:
            theme_name: Name of theme to set

        Returns:
            True if theme was set successfully, False if theme not found
        """
        if theme_name in THEMES:
            self.current_theme = THEMES[theme_name]
            return True
        return False

    def get_color(self, key: str, default: str = "white") -> str:
        """Get a color from the current theme.

        Args:
            key: Color key to retrieve
            default: Default color if key not found

        Returns:
            Color style string
        """
        return self.current_theme.get_color(key, default)

    def get_colors_dict(self) -> Dict[str, str]:
        """Get the complete color dictionary for the current theme.

        Returns:
            Dictionary of all colors in current theme
        """
        return self.current_theme.colors.copy()

    def list_themes(self) -> Dict[str, str]:
        """List all available themes with their descriptions.

        Returns:
            Dictionary mapping theme names to descriptions
        """
        return {name: theme.description for name, theme in THEMES.items()}

    def preview_theme(self, theme_name: str) -> None:
        """Preview a theme by displaying its colors.

        Args:
            theme_name: Name of theme to preview
        """
        from rich.console import Console
        from rich.table import Table
        from rich import box

        theme = self.get_theme(theme_name)
        console = Console()

        console.print(f"\n[bold]Theme: {theme.name}[/bold]")
        console.print(f"[dim]{theme.description}[/dim]\n")

        table = Table(box=box.ROUNDED, show_header=True, header_style="bold")
        table.add_column("Color Key", style="cyan")
        table.add_column("Example", style="white")

        for key, color_value in sorted(theme.colors.items()):
            table.add_row(key, f"[{color_value}]Sample text[/{color_value}]")

        console.print(table)


# Global theme manager instance
_theme_manager_instance = None


def get_theme_manager(theme_name: str = "default") -> ThemeManager:
    """Get the global theme manager instance.

    Args:
        theme_name: Initial theme name (only used on first call)

    Returns:
        ThemeManager instance
    """
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager(theme_name)
    return _theme_manager_instance


def apply_theme_to_visual(theme_name: str) -> bool:
    """Apply a theme to the visual module.

    Args:
        theme_name: Name of theme to apply

    Returns:
        True if successful, False if theme not found
    """
    from utils import visual

    theme_manager = get_theme_manager()
    if theme_manager.set_theme(theme_name):
        # Update the visual module's COLORS dictionary
        visual.COLORS = theme_manager.get_colors_dict()
        # Update the preferences theme name
        visual.preferences.theme = theme_name
        return True
    return False

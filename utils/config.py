"""Configuration management for math_cli with user preferences."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manage user configuration and preferences."""

    def __init__(self):
        """Initialize the configuration manager."""
        # Set up config directory
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"

        # Default configuration
        self.defaults = {
            "theme": "default",
            "colors_enabled": True,
            "animations_enabled": True,
            "show_tips": True,
            "show_toolbar": True,
            "history_limit": 1000,
            "auto_save_history": True,
            "auto_save_session": False,
            "tab_complete_on_type": False,
            "show_operation_count": True,
            "date_format": "%Y-%m-%d %H:%M:%S",
            "number_format": "auto",  # auto, comma, scientific, raw
            "decimal_places": 6,
        }

        # Load or create configuration
        self.config = self._load_config()

    def _get_config_dir(self) -> Path:
        """Get the configuration directory path.

        Returns:
            Path to the configuration directory
        """
        # Use XDG_CONFIG_HOME if available, otherwise ~/.config
        if os.name == 'nt':
            # Windows: use APPDATA
            base_dir = Path(os.environ.get('APPDATA', Path.home()))
        else:
            # Unix-like: use XDG_CONFIG_HOME or ~/.config
            base_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))

        config_dir = base_dir / 'math_cli'

        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        return config_dir

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)

                # Merge with defaults (user config takes precedence)
                config = self.defaults.copy()
                config.update(user_config)

                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                print("Using default configuration")
                return self.defaults.copy()
        else:
            # Create default config file
            self._save_config(self.defaults)
            return self.defaults.copy()

    def _save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file.

        Args:
            config: Configuration to save (uses self.config if None)

        Returns:
            True if successful, False otherwise
        """
        if config is None:
            config = self.config

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any, save: bool = True) -> bool:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
            save: Whether to save to file immediately

        Returns:
            True if successful, False otherwise
        """
        self.config[key] = value

        if save:
            return self._save_config()

        return True

    def update(self, updates: Dict[str, Any], save: bool = True) -> bool:
        """Update multiple configuration values.

        Args:
            updates: Dictionary of updates
            save: Whether to save to file immediately

        Returns:
            True if successful, False otherwise
        """
        self.config.update(updates)

        if save:
            return self._save_config()

        return True

    def reset(self, save: bool = True) -> bool:
        """Reset configuration to defaults.

        Args:
            save: Whether to save to file immediately

        Returns:
            True if successful, False otherwise
        """
        self.config = self.defaults.copy()

        if save:
            return self._save_config()

        return True

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.

        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()

    def show_config(self):
        """Display current configuration in a readable format."""
        from utils.visual import console, preferences
        from rich.table import Table
        from rich import box

        if not preferences.colors_enabled:
            print("\nCurrent Configuration:")
            for key, value in sorted(self.config.items()):
                print(f"  {key}: {value}")
            print(f"\nConfig file: {self.config_file}")
            return

        table = Table(
            title="Math CLI Configuration",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Setting", style="yellow")
        table.add_column("Value", style="green")

        for key, value in sorted(self.config.items()):
            # Format value nicely
            if isinstance(value, bool):
                value_str = "✓" if value else "✗"
                style = "green" if value else "red"
            else:
                value_str = str(value)
                style = "white"

            table.add_row(key, f"[{style}]{value_str}[/{style}]")

        console.print(table)
        console.print(f"\n[dim]Config file: {self.config_file}[/dim]")


# Global configuration instance
_config_instance = None


def get_config() -> ConfigManager:
    """Get the global configuration instance.

    Returns:
        ConfigManager instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance

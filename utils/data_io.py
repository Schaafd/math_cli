"""Data import/export utilities for Math CLI.

This module provides functionality to:
- Load data from CSV and JSON files
- Export data to CSV and JSON formats
- Preview and inspect datasets
- Validate data integrity
"""

import pandas as pd
import json
from pathlib import Path
from typing import Union, Dict, List, Any, Optional
from rich.console import Console
from rich.table import Table

console = Console()


class DataManager:
    """Manages data import/export operations."""

    def __init__(self):
        """Initialize the data manager."""
        self.loaded_datasets = {}  # Store loaded datasets by name

    def load_csv(self, filepath: str, name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Load data from a CSV file.

        Args:
            filepath: Path to the CSV file
            name: Optional name to store the dataset
            **kwargs: Additional arguments passed to pandas.read_csv

        Returns:
            DataFrame containing the loaded data

        Example:
            df = manager.load_csv('data.csv', name='mydata')
        """
        try:
            df = pd.read_csv(filepath, **kwargs)

            # Store dataset if name provided
            if name:
                self.loaded_datasets[name] = df
                console.print(f"[green]✓[/green] Loaded CSV '{filepath}' as '{name}'")

            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")

    def load_json(self, filepath: str, name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Load data from a JSON file.

        Args:
            filepath: Path to the JSON file
            name: Optional name to store the dataset
            **kwargs: Additional arguments passed to pandas.read_json

        Returns:
            DataFrame containing the loaded data

        Example:
            df = manager.load_json('data.json', name='mydata')
        """
        try:
            df = pd.read_json(filepath, **kwargs)

            # Store dataset if name provided
            if name:
                self.loaded_datasets[name] = df
                console.print(f"[green]✓[/green] Loaded JSON '{filepath}' as '{name}'")

            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error loading JSON: {e}")

    def save_csv(self, data: Union[pd.DataFrame, List, Dict], filepath: str, **kwargs) -> None:
        """Save data to a CSV file.

        Args:
            data: DataFrame, list, or dictionary to save
            filepath: Path where to save the CSV
            **kwargs: Additional arguments passed to DataFrame.to_csv

        Example:
            manager.save_csv(df, 'output.csv', index=False)
        """
        try:
            # Convert to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)

            # Set defaults
            kwargs.setdefault('index', False)

            data.to_csv(filepath, **kwargs)
            console.print(f"[green]✓[/green] Saved data to '{filepath}'")
        except Exception as e:
            raise ValueError(f"Error saving CSV: {e}")

    def save_json(self, data: Union[pd.DataFrame, List, Dict], filepath: str, **kwargs) -> None:
        """Save data to a JSON file.

        Args:
            data: DataFrame, list, or dictionary to save
            filepath: Path where to save the JSON
            **kwargs: Additional arguments passed to DataFrame.to_json or json.dump

        Example:
            manager.save_json(df, 'output.json', orient='records')
        """
        try:
            if isinstance(data, pd.DataFrame):
                # Set defaults for DataFrame
                kwargs.setdefault('orient', 'records')
                kwargs.setdefault('indent', 2)
                data.to_json(filepath, **kwargs)
            else:
                # Handle dict/list
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=kwargs.get('indent', 2))

            console.print(f"[green]✓[/green] Saved data to '{filepath}'")
        except Exception as e:
            raise ValueError(f"Error saving JSON: {e}")

    def preview(self, data: Union[pd.DataFrame, str], rows: int = 10) -> None:
        """Preview a dataset in the console.

        Args:
            data: DataFrame or name of stored dataset
            rows: Number of rows to display

        Example:
            manager.preview('mydata', rows=5)
        """
        # Get DataFrame
        if isinstance(data, str):
            if data not in self.loaded_datasets:
                raise ValueError(f"Dataset '{data}' not found. Available: {list(self.loaded_datasets.keys())}")
            df = self.loaded_datasets[data]
        else:
            df = data

        # Create rich table
        table = Table(title=f"Data Preview (first {rows} rows)")

        # Add columns
        for col in df.columns:
            table.add_column(str(col), style="cyan")

        # Add rows
        for idx, row in df.head(rows).iterrows():
            table.add_row(*[str(val) for val in row])

        console.print(table)

    def describe(self, data: Union[pd.DataFrame, str]) -> pd.DataFrame:
        """Get statistical summary of a dataset.

        Args:
            data: DataFrame or name of stored dataset

        Returns:
            DataFrame with statistical summary

        Example:
            summary = manager.describe('mydata')
        """
        # Get DataFrame
        if isinstance(data, str):
            if data not in self.loaded_datasets:
                raise ValueError(f"Dataset '{data}' not found")
            df = self.loaded_datasets[data]
        else:
            df = data

        return df.describe()

    def info(self, data: Union[pd.DataFrame, str]) -> Dict[str, Any]:
        """Get information about a dataset.

        Args:
            data: DataFrame or name of stored dataset

        Returns:
            Dictionary with dataset information

        Example:
            info = manager.info('mydata')
        """
        # Get DataFrame
        if isinstance(data, str):
            if data not in self.loaded_datasets:
                raise ValueError(f"Dataset '{data}' not found")
            df = self.loaded_datasets[data]
        else:
            df = data

        return {
            'shape': df.shape,
            'rows': df.shape[0],
            'columns': df.shape[1],
            'column_names': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'memory_usage': df.memory_usage(deep=True).sum(),
            'missing_values': df.isnull().sum().to_dict()
        }

    def get_dataset(self, name: str) -> pd.DataFrame:
        """Retrieve a stored dataset by name.

        Args:
            name: Name of the dataset

        Returns:
            DataFrame

        Raises:
            ValueError: If dataset not found
        """
        if name not in self.loaded_datasets:
            raise ValueError(f"Dataset '{name}' not found. Available: {list(self.loaded_datasets.keys())}")
        return self.loaded_datasets[name]

    def list_datasets(self) -> List[str]:
        """List all stored datasets.

        Returns:
            List of dataset names
        """
        return list(self.loaded_datasets.keys())

    def remove_dataset(self, name: str) -> None:
        """Remove a stored dataset.

        Args:
            name: Name of the dataset to remove
        """
        if name in self.loaded_datasets:
            del self.loaded_datasets[name]
            console.print(f"[green]✓[/green] Removed dataset '{name}'")
        else:
            console.print(f"[yellow]⚠[/yellow] Dataset '{name}' not found")


# Global data manager instance
_data_manager = None


def get_data_manager() -> DataManager:
    """Get the global data manager instance.

    Returns:
        DataManager instance
    """
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager

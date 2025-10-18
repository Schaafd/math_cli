"""Data transformation operations plugin for Math CLI.

This plugin provides data manipulation and transformation capabilities including:
- Filtering
- Sorting
- Column selection
- Normalization
- Binning
- Aggregation
"""

from core.base_operations import MathOperation
import pandas as pd
import numpy as np
from typing import Union, List, Any
from utils.data_io import get_data_manager


class FilterDataOperation(MathOperation):
    """Filter rows based on a condition."""

    name = "filter_data"
    args = ["dataset", "column", "operator", "value", "?result_name"]
    help = "Filter data: filter_data mydata price > 100 filtered"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, column: str, operator: str,
                value: Union[float, str], result_name: str = None) -> str:
        """Filter dataset rows.

        Args:
            dataset: Name of the loaded dataset
            column: Column to filter on
            operator: Comparison operator (>, <, >=, <=, ==, !=)
            value: Value to compare against
            result_name: Name to save filtered dataset

        Returns:
            Success message with row count
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        # Apply filter based on operator
        if operator == '>':
            filtered_df = df[df[column] > float(value)]
        elif operator == '<':
            filtered_df = df[df[column] < float(value)]
        elif operator == '>=':
            filtered_df = df[df[column] >= float(value)]
        elif operator == '<=':
            filtered_df = df[df[column] <= float(value)]
        elif operator == '==':
            # Try numeric comparison first, fall back to string
            try:
                filtered_df = df[df[column] == float(value)]
            except (ValueError, TypeError):
                filtered_df = df[df[column] == value]
        elif operator == '!=':
            try:
                filtered_df = df[df[column] != float(value)]
            except (ValueError, TypeError):
                filtered_df = df[df[column] != value]
        else:
            raise ValueError(f"Unknown operator: {operator}")

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = filtered_df

        return f"Filtered to {len(filtered_df)} rows (from {len(df)} rows)"


class SortDataOperation(MathOperation):
    """Sort dataset by column(s)."""

    name = "sort_data"
    args = ["dataset", "column", "?ascending", "?result_name"]
    help = "Sort data: sort_data mydata price false sorted"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, column: str,
                ascending: Union[bool, str] = True, result_name: str = None) -> str:
        """Sort dataset.

        Args:
            dataset: Name of the loaded dataset
            column: Column to sort by
            ascending: Sort direction (true/false)
            result_name: Name to save sorted dataset

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        # Convert string to bool if needed
        if isinstance(ascending, str):
            ascending = ascending.lower() in ('true', '1', 'yes')

        sorted_df = df.sort_values(by=column, ascending=ascending)

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = sorted_df

        return f"Sorted {len(sorted_df)} rows by '{column}' ({'ascending' if ascending else 'descending'})"


class SelectColumnsOperation(MathOperation):
    """Select specific columns from dataset."""

    name = "select_columns"
    args = ["dataset", "*columns"]
    help = "Select columns: select_columns mydata name price category"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, *columns) -> pd.DataFrame:
        """Select columns.

        Args:
            dataset: Name of the loaded dataset
            *columns: Column names to select

        Returns:
            DataFrame with selected columns
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        # Validate columns
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise ValueError(f"Columns not found: {missing}")

        return df[list(columns)]


class NormalizeDataOperation(MathOperation):
    """Normalize numeric columns to 0-1 range."""

    name = "normalize_data"
    args = ["dataset", "?method", "?result_name"]
    help = "Normalize: normalize_data mydata minmax normalized"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, method: str = 'minmax',
                result_name: str = None) -> str:
        """Normalize numeric columns.

        Args:
            dataset: Name of the loaded dataset
            method: Normalization method ('minmax' or 'zscore')
            result_name: Name to save normalized dataset

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset).copy()

        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns to normalize")

        # Apply normalization
        if method == 'minmax':
            for col in numeric_cols:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
        elif method == 'zscore':
            for col in numeric_cols:
                mean_val = df[col].mean()
                std_val = df[col].std()
                if std_val > 0:
                    df[col] = (df[col] - mean_val) / std_val
        else:
            raise ValueError(f"Unknown normalization method: {method}")

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = df

        return f"Normalized {len(numeric_cols)} columns using {method}"


class BinDataOperation(MathOperation):
    """Bin continuous data into discrete bins."""

    name = "bin_data"
    args = ["dataset", "column", "bins", "?result_name"]
    help = "Bin data: bin_data mydata age 5 binned"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, column: str, bins: int,
                result_name: str = None) -> str:
        """Bin continuous data.

        Args:
            dataset: Name of the loaded dataset
            column: Column to bin
            bins: Number of bins
            result_name: Name to save result

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset).copy()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        # Create bins
        df[f'{column}_binned'] = pd.cut(df[column], bins=int(bins))

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = df

        return f"Created {bins} bins for column '{column}'"


class AggregateDataOperation(MathOperation):
    """Aggregate all rows using a function."""

    name = "aggregate_data"
    args = ["dataset", "function"]
    help = "Aggregate: aggregate_data mydata mean"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, function: str) -> pd.Series:
        """Aggregate all numeric columns.

        Args:
            dataset: Name of the loaded dataset
            function: Aggregation function (mean, sum, min, max, std, median)

        Returns:
            Series with aggregated values
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        # Get numeric columns
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            raise ValueError("No numeric columns to aggregate")

        # Apply aggregation
        agg_funcs = {
            'mean': 'mean',
            'sum': 'sum',
            'min': 'min',
            'max': 'max',
            'std': 'std',
            'median': 'median',
            'count': 'count'
        }

        if function not in agg_funcs:
            raise ValueError(f"Unknown function: {function}")

        return numeric_df.agg(agg_funcs[function])


class DropNullOperation(MathOperation):
    """Drop rows with null values."""

    name = "drop_nulls"
    args = ["dataset", "?result_name"]
    help = "Drop nulls: drop_nulls mydata cleaned"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, result_name: str = None) -> str:
        """Drop rows with any null values.

        Args:
            dataset: Name of the loaded dataset
            result_name: Name to save cleaned dataset

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        original_count = len(df)
        cleaned_df = df.dropna()

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = cleaned_df

        dropped = original_count - len(cleaned_df)
        return f"Dropped {dropped} rows with null values ({len(cleaned_df)} rows remain)"


class FillNullOperation(MathOperation):
    """Fill null values with a specified value or method."""

    name = "fill_nulls"
    args = ["dataset", "value_or_method", "?result_name"]
    help = "Fill nulls: fill_nulls mydata mean filled"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, value_or_method: str,
                result_name: str = None) -> str:
        """Fill null values.

        Args:
            dataset: Name of the loaded dataset
            value_or_method: Fill value or method (mean, median, mode, 0)
            result_name: Name to save filled dataset

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset).copy()

        null_count = df.isnull().sum().sum()

        # Fill based on method
        if value_or_method == 'mean':
            df = df.fillna(df.mean(numeric_only=True))
        elif value_or_method == 'median':
            df = df.fillna(df.median(numeric_only=True))
        elif value_or_method == 'mode':
            df = df.fillna(df.mode().iloc[0])
        else:
            # Try as numeric value
            try:
                df = df.fillna(float(value_or_method))
            except ValueError:
                # Use as string
                df = df.fillna(value_or_method)

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = df

        return f"Filled {null_count} null values with {value_or_method}"


class RenameColumnOperation(MathOperation):
    """Rename a column."""

    name = "rename_column"
    args = ["dataset", "old_name", "new_name", "?result_name"]
    help = "Rename: rename_column mydata old_col new_col renamed"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, old_name: str, new_name: str,
                result_name: str = None) -> str:
        """Rename a column.

        Args:
            dataset: Name of the loaded dataset
            old_name: Current column name
            new_name: New column name
            result_name: Name to save result

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset).copy()

        if old_name not in df.columns:
            raise ValueError(f"Column '{old_name}' not found")

        df = df.rename(columns={old_name: new_name})

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = df

        return f"Renamed '{old_name}' to '{new_name}'"


class AddColumnOperation(MathOperation):
    """Add a new column with constant value."""

    name = "add_column"
    args = ["dataset", "column_name", "value", "?result_name"]
    help = "Add column: add_column mydata status active modified"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, column_name: str, value: Union[str, float],
                result_name: str = None) -> str:
        """Add a new column.

        Args:
            dataset: Name of the loaded dataset
            column_name: Name of new column
            value: Value for all rows
            result_name: Name to save result

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset).copy()

        # Try numeric conversion
        try:
            value = float(value)
        except (ValueError, TypeError):
            pass

        df[column_name] = value

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = df

        return f"Added column '{column_name}' with value '{value}'"


class SampleDataOperation(MathOperation):
    """Randomly sample rows from dataset."""

    name = "sample_data"
    args = ["dataset", "n", "?result_name"]
    help = "Sample data: sample_data mydata 100 sample"
    category = "data_transform"

    @classmethod
    def execute(cls, dataset: str, n: int, result_name: str = None) -> str:
        """Randomly sample rows.

        Args:
            dataset: Name of the loaded dataset
            n: Number of rows to sample
            result_name: Name to save sample

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        n = int(n)
        if n > len(df):
            n = len(df)

        sample_df = df.sample(n=n, random_state=42)

        # Save if name provided
        if result_name:
            manager.loaded_datasets[result_name] = sample_df

        return f"Sampled {n} rows from {len(df)} total rows"


# All operations are automatically discovered by the plugin manager

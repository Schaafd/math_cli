"""Data analysis operations plugin for Math CLI.

This plugin provides advanced data analysis capabilities including:
- Statistical summaries
- Correlation analysis
- Group-by operations
- Outlier detection
- Time series analysis
"""

from core.base_operations import MathOperation
import pandas as pd
import numpy as np
from typing import Union, List, Dict, Any
from utils.data_io import get_data_manager


class LoadDataOperation(MathOperation):
    """Load data from a file."""

    name = "load_data"
    args = ["filepath", "?format", "?name"]
    help = "Load data: load_data 'data.csv' csv mydata"
    category = "data_analysis"

    @classmethod
    def execute(cls, filepath: str, format: str = None, name: str = None) -> str:
        """Load data from CSV or JSON file.

        Args:
            filepath: Path to the data file
            format: File format ('csv' or 'json'), auto-detected if not provided
            name: Name to store the dataset

        Returns:
            Success message with dataset info
        """
        manager = get_data_manager()

        # Auto-detect format if not provided
        if format is None:
            if filepath.endswith('.csv'):
                format = 'csv'
            elif filepath.endswith('.json'):
                format = 'json'
            else:
                raise ValueError("Cannot detect format. Please specify 'csv' or 'json'")

        # Load based on format
        if format.lower() == 'csv':
            df = manager.load_csv(filepath, name=name)
        elif format.lower() == 'json':
            df = manager.load_json(filepath, name=name)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return f"Loaded {df.shape[0]} rows × {df.shape[1]} columns"


class DataDescribeOperation(MathOperation):
    """Generate statistical summary of a dataset."""

    name = "describe_data"
    args = ["dataset"]
    help = "Statistical summary: describe_data mydata"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str) -> pd.DataFrame:
        """Get statistical summary.

        Args:
            dataset: Name of the loaded dataset

        Returns:
            DataFrame with statistical summary
        """
        manager = get_data_manager()
        return manager.describe(dataset)


class CorrelationMatrixOperation(MathOperation):
    """Calculate correlation matrix for a dataset."""

    name = "correlation_matrix"
    args = ["dataset", "?method"]
    help = "Correlation matrix: correlation_matrix mydata pearson"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation matrix.

        Args:
            dataset: Name of the loaded dataset
            method: Correlation method ('pearson', 'kendall', 'spearman')

        Returns:
            Correlation matrix
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            raise ValueError("Dataset has no numeric columns")

        return numeric_df.corr(method=method)


class GroupByOperation(MathOperation):
    """Group data and calculate aggregations."""

    name = "groupby"
    args = ["dataset", "column", "?agg_func"]
    help = "Group by: groupby mydata category mean"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, column: str, agg_func: str = 'mean') -> pd.DataFrame:
        """Group data and aggregate.

        Args:
            dataset: Name of the loaded dataset
            column: Column to group by
            agg_func: Aggregation function (mean, sum, count, min, max, std)

        Returns:
            Grouped and aggregated data
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataset")

        # Map aggregation function
        agg_funcs = {
            'mean': 'mean',
            'sum': 'sum',
            'count': 'count',
            'min': 'min',
            'max': 'max',
            'std': 'std',
            'median': 'median'
        }

        if agg_func not in agg_funcs:
            raise ValueError(f"Unknown aggregation function: {agg_func}")

        return df.groupby(column).agg(agg_funcs[agg_func])


class OutlierDetectionOperation(MathOperation):
    """Detect outliers using IQR method."""

    name = "detect_outliers"
    args = ["dataset", "column", "?threshold"]
    help = "Detect outliers: detect_outliers mydata price 1.5"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, column: str, threshold: float = 1.5) -> Dict[str, Any]:
        """Detect outliers using IQR method.

        Args:
            dataset: Name of the loaded dataset
            column: Column to analyze
            threshold: IQR multiplier threshold (default 1.5)

        Returns:
            Dictionary with outlier information
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataset")

        data = df[column].dropna()

        if not np.issubdtype(data.dtype, np.number):
            raise ValueError(f"Column '{column}' must be numeric")

        # Calculate IQR
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1

        # Define outlier bounds
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        # Find outliers
        outliers = data[(data < lower_bound) | (data > upper_bound)]

        return {
            'n_outliers': len(outliers),
            'outlier_percentage': (len(outliers) / len(data)) * 100,
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'outlier_values': outliers.tolist()[:20]  # Limit to first 20
        }


class MissingValuesOperation(MathOperation):
    """Analyze missing values in a dataset."""

    name = "missing_values"
    args = ["dataset"]
    help = "Missing values analysis: missing_values mydata"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str) -> pd.DataFrame:
        """Analyze missing values.

        Args:
            dataset: Name of the loaded dataset

        Returns:
            DataFrame with missing value counts and percentages
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        missing_count = df.isnull().sum()
        missing_percent = (missing_count / len(df)) * 100

        result = pd.DataFrame({
            'missing_count': missing_count,
            'missing_percent': missing_percent
        })

        return result[result['missing_count'] > 0].sort_values('missing_count', ascending=False)


class UniqueValuesOperation(MathOperation):
    """Count unique values in a column."""

    name = "unique_values"
    args = ["dataset", "column"]
    help = "Count unique: unique_values mydata category"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, column: str) -> Dict[str, Any]:
        """Count unique values in a column.

        Args:
            dataset: Name of the loaded dataset
            column: Column to analyze

        Returns:
            Dictionary with unique value counts
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataset")

        value_counts = df[column].value_counts()

        return {
            'n_unique': len(value_counts),
            'top_values': value_counts.head(10).to_dict()
        }


class CrosstabOperation(MathOperation):
    """Create crosstab (contingency table) of two columns."""

    name = "crosstab"
    args = ["dataset", "column1", "column2"]
    help = "Crosstab: crosstab mydata category region"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, column1: str, column2: str) -> pd.DataFrame:
        """Create crosstab.

        Args:
            dataset: Name of the loaded dataset
            column1: First column
            column2: Second column

        Returns:
            Crosstab DataFrame
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        if column1 not in df.columns:
            raise ValueError(f"Column '{column1}' not found")
        if column2 not in df.columns:
            raise ValueError(f"Column '{column2}' not found")

        return pd.crosstab(df[column1], df[column2])


class PivotTableOperation(MathOperation):
    """Create pivot table."""

    name = "pivot_table"
    args = ["dataset", "values", "index", "?columns", "?aggfunc"]
    help = "Pivot: pivot_table mydata sales region product mean"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, values: str, index: str,
                columns: str = None, aggfunc: str = 'mean') -> pd.DataFrame:
        """Create pivot table.

        Args:
            dataset: Name of the loaded dataset
            values: Column with values to aggregate
            index: Column for row index
            columns: Column for column headers (optional)
            aggfunc: Aggregation function

        Returns:
            Pivot table
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        kwargs = {
            'values': values,
            'index': index,
            'aggfunc': aggfunc
        }

        if columns:
            kwargs['columns'] = columns

        return pd.pivot_table(df, **kwargs)


class DataInfoOperation(MathOperation):
    """Get detailed information about a dataset."""

    name = "data_info"
    args = ["dataset"]
    help = "Dataset info: data_info mydata"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str) -> Dict[str, Any]:
        """Get dataset information.

        Args:
            dataset: Name of the loaded dataset

        Returns:
            Dictionary with dataset information
        """
        manager = get_data_manager()
        return manager.info(dataset)


class ListDatasetsOperation(MathOperation):
    """List all loaded datasets."""

    name = "list_datasets"
    args = []
    help = "List datasets: list_datasets"
    category = "data_analysis"

    @classmethod
    def execute(cls) -> List[str]:
        """List all loaded datasets.

        Returns:
            List of dataset names
        """
        manager = get_data_manager()
        datasets = manager.list_datasets()

        if not datasets:
            return ["No datasets loaded"]

        return datasets


class SaveDataOperation(MathOperation):
    """Save a dataset to a file."""

    name = "save_data"
    args = ["dataset", "filepath", "?format"]
    help = "Save data: save_data mydata 'output.csv' csv"
    category = "data_analysis"

    @classmethod
    def execute(cls, dataset: str, filepath: str, format: str = None) -> str:
        """Save dataset to file.

        Args:
            dataset: Name of the loaded dataset
            filepath: Path where to save
            format: File format ('csv' or 'json'), auto-detected if not provided

        Returns:
            Success message
        """
        manager = get_data_manager()
        df = manager.get_dataset(dataset)

        # Auto-detect format if not provided
        if format is None:
            if filepath.endswith('.csv'):
                format = 'csv'
            elif filepath.endswith('.json'):
                format = 'json'
            else:
                raise ValueError("Cannot detect format. Please specify 'csv' or 'json'")

        # Save based on format
        if format.lower() == 'csv':
            manager.save_csv(df, filepath)
        elif format.lower() == 'json':
            manager.save_json(df, filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return f"Saved to {filepath}"


# All operations are automatically discovered by the plugin manager

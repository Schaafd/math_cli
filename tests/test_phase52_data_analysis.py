"""Tests for Phase 5.2: Data Analysis & Visualization."""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path

from utils.data_io import DataManager, get_data_manager
from utils.advanced_plotting import (
    StatisticalPlotter,
    plot_histogram,
    plot_boxplot,
    plot_scatter_regression,
    plot_heatmap
)
from core.plugin_manager import PluginManager


class TestDataManager:
    """Test data I/O operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = DataManager()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_csv(self):
        """Test loading CSV data."""
        # Create test CSV
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        test_data.to_csv(csv_path, index=False)

        # Load CSV
        df = self.manager.load_csv(csv_path, name='test')
        assert len(df) == 3
        assert list(df.columns) == ['A', 'B']
        assert 'test' in self.manager.loaded_datasets

    def test_load_json(self):
        """Test loading JSON data."""
        # Create test JSON
        json_path = os.path.join(self.temp_dir, 'test.json')
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        test_data.to_json(json_path, orient='records')

        # Load JSON
        df = self.manager.load_json(json_path, name='test')
        assert len(df) == 3
        assert 'test' in self.manager.loaded_datasets

    def test_save_csv(self):
        """Test saving to CSV."""
        csv_path = os.path.join(self.temp_dir, 'output.csv')
        test_data = pd.DataFrame({'A': [1, 2, 3]})

        self.manager.save_csv(test_data, csv_path)
        assert os.path.exists(csv_path)

        # Verify content
        loaded = pd.read_csv(csv_path)
        assert len(loaded) == 3

    def test_save_json(self):
        """Test saving to JSON."""
        json_path = os.path.join(self.temp_dir, 'output.json')
        test_data = pd.DataFrame({'A': [1, 2, 3]})

        self.manager.save_json(test_data, json_path)
        assert os.path.exists(json_path)

    def test_describe(self):
        """Test statistical description."""
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
        self.manager.loaded_datasets['test'] = df

        desc = self.manager.describe('test')
        assert 'mean' in desc.index
        assert desc.loc['mean', 'A'] == 3.0

    def test_info(self):
        """Test dataset info."""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
        self.manager.loaded_datasets['test'] = df

        info = self.manager.info('test')
        assert info['rows'] == 3
        assert info['columns'] == 2
        assert 'A' in info['column_names']

    def test_get_dataset(self):
        """Test retrieving dataset."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        self.manager.loaded_datasets['test'] = df

        retrieved = self.manager.get_dataset('test')
        pd.testing.assert_frame_equal(df, retrieved)

    def test_list_datasets(self):
        """Test listing datasets."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        self.manager.loaded_datasets['test1'] = df
        self.manager.loaded_datasets['test2'] = df

        datasets = self.manager.list_datasets()
        assert 'test1' in datasets
        assert 'test2' in datasets

    def test_remove_dataset(self):
        """Test removing dataset."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        self.manager.loaded_datasets['test'] = df

        self.manager.remove_dataset('test')
        assert 'test' not in self.manager.loaded_datasets


class TestStatisticalPlotter:
    """Test advanced plotting functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.plotter = StatisticalPlotter(width=60, height=20)
        self.test_data = np.random.randn(100)

    def test_histogram(self):
        """Test histogram plotting."""
        result = self.plotter.histogram(self.test_data, bins=10)
        assert "Histogram" in result
        assert "─" in result
        assert "Min:" in result
        assert "Max:" in result

    def test_histogram_with_series(self):
        """Test histogram with pandas Series."""
        series = pd.Series(self.test_data)
        result = self.plotter.histogram(series, bins=10)
        assert "Histogram" in result

    def test_boxplot(self):
        """Test box plot."""
        result = self.plotter.boxplot(self.test_data, label="Test")
        assert "Box Plot" in result
        assert "Q1:" in result
        assert "Median:" in result
        assert "Q3:" in result
        assert "IQR:" in result

    def test_scatter_with_regression(self):
        """Test scatter plot with regression line."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 5, 4, 5])

        result = self.plotter.scatter_with_regression(x, y)
        assert "Scatter Plot" in result
        assert "R²" in result

    def test_heatmap(self):
        """Test heatmap."""
        data = np.array([[1.0, 0.8], [0.8, 1.0]])
        labels = ['A', 'B']

        result = self.plotter.heatmap(data, labels=labels)
        assert "Heatmap" in result
        assert "Scale:" in result

    def test_heatmap_with_dataframe(self):
        """Test heatmap with DataFrame."""
        df = pd.DataFrame({
            'A': [1.0, 0.8],
            'B': [0.8, 1.0]
        })

        result = self.plotter.heatmap(df)
        assert "Heatmap" in result

    def test_distribution_plot(self):
        """Test distribution plot."""
        result = self.plotter.distribution_plot(self.test_data)
        assert "Histogram" in result  # Currently uses histogram

    def test_plot_histogram_function(self):
        """Test convenience histogram function."""
        result = plot_histogram(self.test_data, bins=5)
        assert "Histogram" in result

    def test_plot_boxplot_function(self):
        """Test convenience boxplot function."""
        result = plot_boxplot(self.test_data)
        assert "Box Plot" in result

    def test_plot_scatter_regression_function(self):
        """Test convenience scatter regression function."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 5, 4, 5])

        result = plot_scatter_regression(x, y)
        assert "Scatter Plot" in result

    def test_plot_heatmap_function(self):
        """Test convenience heatmap function."""
        data = np.array([[1.0, 0.5], [0.5, 1.0]])
        result = plot_heatmap(data)
        assert "Heatmap" in result


class TestDataAnalysisOperations:
    """Test data analysis plugin operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

        # Create test data
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.temp_dir, 'test.csv')

        test_data = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 10, 20],
            'category': ['A', 'A', 'B', 'B', 'C', 'C', 'C'],
            'score': [10, 20, 30, 40, 50, 60, 70]
        })
        test_data.to_csv(self.csv_path, index=False)

    def teardown_method(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

        # Clear loaded datasets
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets.clear()

    def test_load_data_csv(self):
        """Test loading CSV data."""
        result = self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')
        assert '7 rows' in result
        assert '3 columns' in result

    def test_describe_data(self):
        """Test data description."""
        # Load data first
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        # Describe
        result = self.manager.execute_operation('describe_data', 'testdata')
        assert isinstance(result, pd.DataFrame)
        assert 'mean' in result.index

    def test_correlation_matrix(self):
        """Test correlation matrix."""
        # Load data
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        # Get correlation
        result = self.manager.execute_operation('correlation_matrix', 'testdata')
        assert isinstance(result, pd.DataFrame)
        assert 'value' in result.columns
        assert 'score' in result.columns

    def test_groupby(self):
        """Test groupby operation."""
        # Load data
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        # Group by
        result = self.manager.execute_operation('groupby', 'testdata', 'category', 'mean')
        assert isinstance(result, pd.DataFrame)

    def test_missing_values(self):
        """Test missing values analysis."""
        # Create data with missing values
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [5, None, None, 8]
        })

        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['test'] = df

        result = self.manager.execute_operation('missing_values', 'test')
        assert isinstance(result, pd.DataFrame)

    def test_unique_values(self):
        """Test unique values counting."""
        # Load data
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        result = self.manager.execute_operation('unique_values', 'testdata', 'category')
        assert 'n_unique' in result
        assert result['n_unique'] == 3

    def test_data_info(self):
        """Test data info."""
        # Load data
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        result = self.manager.execute_operation('data_info', 'testdata')
        assert 'rows' in result
        assert result['rows'] == 7

    def test_list_datasets(self):
        """Test listing datasets."""
        # Load data
        self.manager.execute_operation('load_data', self.csv_path, 'csv', 'testdata')

        result = self.manager.execute_operation('list_datasets')
        assert 'testdata' in result


class TestDataTransformOperations:
    """Test data transformation plugin operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

        # Create test data
        df = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 10, 20],
            'category': ['A', 'A', 'B', 'B', 'C', 'C', 'C'],
            'score': [10, 20, 30, 40, 50, 60, 70]
        })

        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['testdata'] = df

    def teardown_method(self):
        """Clean up."""
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets.clear()

    def test_filter_data(self):
        """Test filtering data."""
        result = self.manager.execute_operation('filter_data', 'testdata', 'value', '>', 3, 'filtered')
        assert 'Filtered to 4 rows' in result

    def test_sort_data(self):
        """Test sorting data."""
        result = self.manager.execute_operation('sort_data', 'testdata', 'value', 'false', 'sorted')
        assert 'Sorted 7 rows' in result
        assert 'descending' in result

    def test_select_columns(self):
        """Test selecting columns."""
        result = self.manager.execute_operation('select_columns', 'testdata', 'value', 'score')
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['value', 'score']

    def test_normalize_data(self):
        """Test normalization."""
        result = self.manager.execute_operation('normalize_data', 'testdata', 'minmax', 'normalized')
        assert 'Normalized 2 columns' in result

    def test_aggregate_data(self):
        """Test aggregation."""
        result = self.manager.execute_operation('aggregate_data', 'testdata', 'mean')
        assert isinstance(result, pd.Series)

    def test_drop_nulls(self):
        """Test dropping nulls."""
        # Create data with nulls
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': [5, 6, 7, 8]
        })
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['nulldata'] = df

        result = self.manager.execute_operation('drop_nulls', 'nulldata', 'cleaned')
        assert 'Dropped 1 rows' in result

    def test_fill_nulls(self):
        """Test filling nulls."""
        # Create data with nulls
        df = pd.DataFrame({
            'A': [1.0, 2.0, None, 4.0],
            'B': [5, 6, 7, 8]
        })
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['nulldata'] = df

        result = self.manager.execute_operation('fill_nulls', 'nulldata', 'mean', 'filled')
        assert 'Filled 1 null' in result

    def test_sample_data(self):
        """Test sampling data."""
        result = self.manager.execute_operation('sample_data', 'testdata', 3, 'sample')
        assert 'Sampled 3 rows' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

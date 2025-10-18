"""Tests for Phase 5.2.5: CLI Plotting Integration."""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from core.plugin_manager import PluginManager
from utils.data_io import get_data_manager


class TestPlottingOperations:
    """Test CLI plotting operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()

        # Create test dataset
        self.test_data = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 10, 20, 15, 12, 8],
            'category': ['A', 'A', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'],
            'score': [10, 20, 30, 40, 50, 60, 70, 55, 45, 35],
            'price': [100, 150, 200, 175, 225, 250, 275, 300, 225, 200]
        })

        # Load into DataManager
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['testdata'] = self.test_data

    def teardown_method(self):
        """Clean up."""
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets.clear()

    def test_plot_hist_basic(self):
        """Test basic histogram plotting."""
        result = self.manager.execute_operation('plot_hist', 'testdata', 'value')
        assert 'Plotted histogram' in result
        assert 'testdata.value' in result

    def test_plot_hist_with_bins(self):
        """Test histogram with custom bins."""
        result = self.manager.execute_operation('plot_hist', 'testdata', 'value', '5')
        assert 'Plotted histogram' in result

    def test_plot_hist_invalid_column(self):
        """Test histogram with invalid column."""
        with pytest.raises(ValueError, match="Column 'invalid' not found"):
            self.manager.execute_operation('plot_hist', 'testdata', 'invalid')

    def test_plot_hist_non_numeric(self):
        """Test histogram with non-numeric column."""
        with pytest.raises(ValueError, match="must be numeric"):
            self.manager.execute_operation('plot_hist', 'testdata', 'category')

    def test_plot_hist_invalid_bins(self):
        """Test histogram with invalid bins parameter."""
        with pytest.raises(ValueError, match="bins must be an integer"):
            self.manager.execute_operation('plot_hist', 'testdata', 'value', 'abc')

    def test_plot_hist_missing_dataset(self):
        """Test histogram with missing dataset."""
        with pytest.raises(ValueError, match="Dataset 'missing' not found"):
            self.manager.execute_operation('plot_hist', 'missing', 'value')

    def test_plot_box_basic(self):
        """Test basic box plot."""
        result = self.manager.execute_operation('plot_box', 'testdata', 'score')
        assert 'Plotted box plot' in result
        assert 'testdata.score' in result

    def test_plot_box_with_label(self):
        """Test box plot with custom label."""
        result = self.manager.execute_operation('plot_box', 'testdata', 'score', 'Test_Scores')
        assert 'Plotted box plot' in result

    def test_plot_box_invalid_column(self):
        """Test box plot with invalid column."""
        with pytest.raises(ValueError, match="Column 'invalid' not found"):
            self.manager.execute_operation('plot_box', 'testdata', 'invalid')

    def test_plot_box_non_numeric(self):
        """Test box plot with non-numeric column."""
        with pytest.raises(ValueError, match="must be numeric"):
            self.manager.execute_operation('plot_box', 'testdata', 'category')

    def test_plot_scatter_basic(self):
        """Test basic scatter plot."""
        result = self.manager.execute_operation('plot_scatter', 'testdata', 'value', 'score')
        assert 'Plotted' in result
        assert 'regression' in result

    def test_plot_scatter_invalid_x_column(self):
        """Test scatter plot with invalid x column."""
        with pytest.raises(ValueError, match="Column 'invalid' not found"):
            self.manager.execute_operation('plot_scatter', 'testdata', 'invalid', 'score')

    def test_plot_scatter_invalid_y_column(self):
        """Test scatter plot with invalid y column."""
        with pytest.raises(ValueError, match="Column 'invalid' not found"):
            self.manager.execute_operation('plot_scatter', 'testdata', 'value', 'invalid')

    def test_plot_scatter_non_numeric_x(self):
        """Test scatter plot with non-numeric x column."""
        with pytest.raises(ValueError, match="must be numeric"):
            self.manager.execute_operation('plot_scatter', 'testdata', 'category', 'score')

    def test_plot_scatter_non_numeric_y(self):
        """Test scatter plot with non-numeric y column."""
        with pytest.raises(ValueError, match="must be numeric"):
            self.manager.execute_operation('plot_scatter', 'testdata', 'value', 'category')

    def test_plot_heatmap_basic(self):
        """Test basic heatmap plotting."""
        result = self.manager.execute_operation('plot_heatmap', 'testdata')
        assert 'Plotted correlation heatmap' in result
        assert 'testdata' in result

    def test_plot_heatmap_missing_dataset(self):
        """Test heatmap with missing dataset."""
        with pytest.raises(ValueError, match="Dataset 'missing' not found"):
            self.manager.execute_operation('plot_heatmap', 'missing')

    def test_plot_heatmap_no_numeric_columns(self):
        """Test heatmap with no numeric columns."""
        # Create dataset with only text columns
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'city': ['NYC', 'LA', 'Chicago']
        })
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['textonly'] = df

        with pytest.raises(ValueError, match="has no numeric columns"):
            self.manager.execute_operation('plot_heatmap', 'textonly')

    def test_plot_hist_operation_metadata(self):
        """Test plot_hist operation has correct metadata."""
        metadata = self.manager.operations['plot_hist'].get_metadata()
        assert metadata['name'] == 'plot_hist'
        assert metadata['category'] == 'visualization'
        assert 'dataset' in metadata['args']
        assert 'column' in metadata['args']

    def test_plot_box_operation_metadata(self):
        """Test plot_box operation has correct metadata."""
        metadata = self.manager.operations['plot_box'].get_metadata()
        assert metadata['name'] == 'plot_box'
        assert metadata['category'] == 'visualization'

    def test_plot_scatter_operation_metadata(self):
        """Test plot_scatter operation has correct metadata."""
        metadata = self.manager.operations['plot_scatter'].get_metadata()
        assert metadata['name'] == 'plot_scatter'
        assert metadata['category'] == 'visualization'
        assert 'dataset' in metadata['args']
        assert 'x_column' in metadata['args']
        assert 'y_column' in metadata['args']

    def test_plot_heatmap_operation_metadata(self):
        """Test plot_heatmap operation has correct metadata."""
        metadata = self.manager.operations['plot_heatmap'].get_metadata()
        assert metadata['name'] == 'plot_heatmap'
        assert metadata['category'] == 'visualization'
        assert 'dataset' in metadata['args']


class TestPlottingIntegration:
    """Test plotting operations with real data workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PluginManager()
        self.manager.discover_plugins()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

        data_mgr = get_data_manager()
        data_mgr.loaded_datasets.clear()

    def test_full_workflow_csv_to_plots(self):
        """Test complete workflow: load CSV, create plots."""
        # Create test CSV
        csv_path = os.path.join(self.temp_dir, 'test_data.csv')
        test_data = pd.DataFrame({
            'temperature': [20, 22, 21, 23, 24, 22, 21, 20, 19, 21],
            'humidity': [50, 55, 52, 60, 65, 58, 54, 51, 48, 53],
            'pressure': [1013, 1015, 1014, 1016, 1017, 1015, 1014, 1013, 1012, 1014]
        })
        test_data.to_csv(csv_path, index=False)

        # Load data
        self.manager.execute_operation('load_data', csv_path, 'csv', 'weather')

        # Create histogram
        result = self.manager.execute_operation('plot_hist', 'weather', 'temperature', '5')
        assert 'Plotted histogram' in result

        # Create box plot
        result = self.manager.execute_operation('plot_box', 'weather', 'humidity')
        assert 'Plotted box plot' in result

        # Create scatter plot
        result = self.manager.execute_operation('plot_scatter', 'weather', 'temperature', 'humidity')
        assert 'regression' in result

        # Create heatmap
        result = self.manager.execute_operation('plot_heatmap', 'weather')
        assert 'heatmap' in result

    def test_plotting_after_filtering(self):
        """Test plotting filtered data."""
        # Create and load test data
        df = pd.DataFrame({
            'value': list(range(1, 101)),
            'squared': [x**2 for x in range(1, 101)]
        })
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['numbers'] = df

        # Filter data
        self.manager.execute_operation('filter_data', 'numbers', 'value', '>', '50', 'filtered')

        # Plot filtered data
        result = self.manager.execute_operation('plot_hist', 'filtered', 'value')
        assert 'Plotted histogram' in result

    def test_plotting_with_missing_values(self):
        """Test plotting with missing values."""
        # Create data with NaN
        df = pd.DataFrame({
            'value': [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10]
        })
        data_mgr = get_data_manager()
        data_mgr.loaded_datasets['with_nans'] = df

        # Histogram should handle NaN
        result = self.manager.execute_operation('plot_hist', 'with_nans', 'value')
        assert 'Plotted histogram' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

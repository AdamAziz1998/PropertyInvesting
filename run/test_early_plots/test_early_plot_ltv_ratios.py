"""
Unit tests for plot_ltv_ratios in investments.run.plots (run/plots.py)
Covers: happy paths, edge cases.
"""

import pytest
import matplotlib
import matplotlib.pyplot as plt

# Use the Agg backend for matplotlib to avoid GUI issues during testing
matplotlib.use("Agg")

from investments.run.plots import plot_ltv_ratios

@pytest.mark.usefixtures("clear_plt")
class TestPlotLtvRatios:
    @pytest.fixture(autouse=True)
    def clear_plt(self):
        """Ensure matplotlib state is clean before each test."""
        plt.close("all")

    # ------------------- Happy Path Tests -------------------

    @pytest.mark.happy_path
    def test_single_property_multiple_months(self, mocker):
        """
        Test plotting with a single property tracked over multiple months.
        """
        history = [
            {"month": 1, "properties": [{"ltv": 0.8}]},
            {"month": 2, "properties": [{"ltv": 0.75}]},
            {"month": 3, "properties": [{"ltv": 0.7}]},
        ]
        # Patch plt.show to prevent actual plot display
        show_mock = mocker.patch("matplotlib.pyplot.show")
        plot_ltv_ratios(history)
        show_mock.assert_called_once()
        # Check that a line was plotted
        assert len(plt.gca().lines) == 1
        # Check label
        assert plt.gca().get_legend().get_texts()[0].get_text() == "Property 1 LTV"

    @pytest.mark.happy_path
    def test_multiple_properties_multiple_months(self, mocker):
        """
        Test plotting with multiple properties tracked over multiple months.
        """
        history = [
            {"month": 1, "properties": [{"ltv": 0.8}, {"ltv": 0.7}]},
            {"month": 2, "properties": [{"ltv": 0.75}, {"ltv": 0.68}]},
            {"month": 3, "properties": [{"ltv": 0.7}, {"ltv": 0.65}]},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        plot_ltv_ratios(history)
        show_mock.assert_called_once()
        # Two lines for two properties
        assert len(plt.gca().lines) == 2
        labels = [t.get_text() for t in plt.gca().get_legend().get_texts()]
        assert "Property 1 LTV" in labels
        assert "Property 2 LTV" in labels

    @pytest.mark.happy_path
    def test_property_ltv_values_varying(self, mocker):
        """
        Test that LTV values are correctly mapped to months for each property.
        """
        history = [
            {"month": 1, "properties": [{"ltv": 0.8}, {"ltv": 0.6}]},
            {"month": 2, "properties": [{"ltv": 0.7}, {"ltv": 0.5}]},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        plot_ltv_ratios(history)
        show_mock.assert_called_once()
        # Check that the plotted data matches the input
        lines = plt.gca().lines
        assert lines[0].get_xdata().tolist() == [1, 2]
        assert lines[0].get_ydata().tolist() == [0.8, 0.7]
        assert lines[1].get_xdata().tolist() == [1, 2]
        assert lines[1].get_ydata().tolist() == [0.6, 0.5]

    # ------------------- Edge Case Tests -------------------

    @pytest.mark.edge_case
    def test_empty_history(self, mocker):
        """
        Test that an empty history raises an IndexError (since history[0] is accessed).
        """
        show_mock = mocker.patch("matplotlib.pyplot.show")
        with pytest.raises(IndexError):
            plot_ltv_ratios([])
        show_mock.assert_not_called()

    @pytest.mark.edge_case
    def test_history_with_no_properties(self, mocker):
        """
        Test that a history with no properties in the first entry raises an IndexError.
        """
        history = [
            {"month": 1, "properties": []},
            {"month": 2, "properties": []},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        with pytest.raises(IndexError):
            plot_ltv_ratios(history)
        show_mock.assert_not_called()

    @pytest.mark.edge_case
    def test_properties_missing_ltv_key(self, mocker):
        """
        Test that missing 'ltv' key in properties raises a KeyError.
        """
        history = [
            {"month": 1, "properties": [{"foo": 1}]},
            {"month": 2, "properties": [{"foo": 2}]},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        with pytest.raises(KeyError):
            plot_ltv_ratios(history)
        show_mock.assert_not_called()

    @pytest.mark.edge_case
    def test_history_with_missing_month_key(self, mocker):
        """
        Test that missing 'month' key in history entries raises a KeyError.
        """
        history = [
            {"foo": 1, "properties": [{"ltv": 0.8}]},
            {"foo": 2, "properties": [{"ltv": 0.7}]},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        with pytest.raises(KeyError):
            plot_ltv_ratios(history)
        show_mock.assert_not_called()

    @pytest.mark.edge_case
    def test_history_with_inconsistent_property_counts(self, mocker):
        """
        Test that inconsistent property counts across history raises an IndexError.
        """
        history = [
            {"month": 1, "properties": [{"ltv": 0.8}, {"ltv": 0.7}]},
            {"month": 2, "properties": [{"ltv": 0.75}]},  # Only one property
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        with pytest.raises(IndexError):
            plot_ltv_ratios(history)
        show_mock.assert_not_called()

    @pytest.mark.edge_case
    def test_history_with_non_numeric_ltv(self, mocker):
        """
        Test that non-numeric LTV values are handled (should plot, but matplotlib may error).
        """
        history = [
            {"month": 1, "properties": [{"ltv": "not_a_number"}]},
            {"month": 2, "properties": [{"ltv": 0.7}]},
        ]
        show_mock = mocker.patch("matplotlib.pyplot.show")
        # matplotlib will raise a ValueError when trying to plot non-numeric data
        with pytest.raises(ValueError):
            plot_ltv_ratios(history)
        show_mock.assert_not_called()
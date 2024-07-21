import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
import sys
from function_plotter import FunctionPlotter  # Ensure function_plotter.py is the name of your main application file

@pytest.fixture
def app(qtbot):
    """Fixture to create the application instance."""
    test_app = QApplication(sys.argv)
    window = FunctionPlotter()
    qtbot.addWidget(window)
    return window

def test_plot_function_valid_input(app, qtbot):
    """Test plotting with valid input."""
    qtbot.keyClicks(app.function_input, "5*x**3 + 2*x")
    qtbot.keyClicks(app.min_x_input, "-10")
    qtbot.keyClicks(app.max_x_input, "10")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    assert app.figure.axes[0].lines, "The plot should have lines"

def test_plot_function_invalid_function(app, qtbot):
    """Test plotting with invalid function input."""
    qtbot.keyClicks(app.function_input, "5*x**3 + 2x")
    qtbot.keyClicks(app.min_x_input, "-10")
    qtbot.keyClicks(app.max_x_input, "10")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    assert not app.figure.axes[0].lines, "The plot should not have lines for invalid function"

def test_plot_function_invalid_min_max(app, qtbot):
    """Test plotting with invalid min/max input."""
    qtbot.keyClicks(app.function_input, "5*x**3 + 2*x")
    qtbot.keyClicks(app.min_x_input, "min")
    qtbot.keyClicks(app.max_x_input, "max")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    assert not app.figure.axes[0].lines, "The plot should not have lines for invalid min/max values"

def test_plot_function_min_greater_than_max(app, qtbot):
    """Test plotting with min x greater than max x."""
    qtbot.keyClicks(app.function_input, "5*x**3 + 2*x")
    qtbot.keyClicks(app.min_x_input, "10")
    qtbot.keyClicks(app.max_x_input, "-10")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    assert not app.figure.axes[0].lines, "The plot should not have lines when min x is greater than max x"

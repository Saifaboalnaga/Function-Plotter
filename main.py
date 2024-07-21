import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QMessageBox, QGridLayout, QStatusBar
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FunctionPlotter(QMainWindow):
    def __init__(self):
        """Initialize the Function Plotter application."""
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout(self.main_widget)

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Function of x (e.g., 5*x^3 + 2*x):"), 0, 0)
        self.function_input = QLineEdit(self)
        grid_layout.addWidget(self.function_input, 0, 1)

        grid_layout.addWidget(QLabel("Min x value:"), 1, 0)
        self.min_x_input = QLineEdit(self)
        self.min_x_input.setPlaceholderText("-10")
        grid_layout.addWidget(self.min_x_input, 1, 1)

        grid_layout.addWidget(QLabel("Max x value:"), 2, 0)
        self.max_x_input = QLineEdit(self)
        self.max_x_input.setPlaceholderText("10")
        grid_layout.addWidget(self.max_x_input, 2, 1)

        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.plot_function)
        grid_layout.addWidget(self.plot_button, 3, 0, 1, 2)

        layout.addLayout(grid_layout)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def plot_function(self):
        """Plot the user-entered function within the specified range."""
        func_str = self.function_input.text()
        min_x_str = self.min_x_input.text() or self.min_x_input.placeholderText()
        max_x_str = self.max_x_input.text() or self.max_x_input.placeholderText()

        if not self.validate_input(func_str, min_x_str, max_x_str):
            return

        min_x = float(min_x_str)
        max_x = float(max_x_str)

        if min_x >= max_x:
            self.show_error("Min x value must be less than Max x value")
            return

        x = np.linspace(min_x, max_x, 400)
        try:
            y = eval(self.convert_function(func_str, x))
        except Exception as e:
            self.show_error(f"Error evaluating function: {e}")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, label=func_str)
        ax.legend()
        self.canvas.draw()

    def validate_input(self, func_str, min_x_str, max_x_str):
        """Validate user input."""
        if not func_str:
            self.show_error("Function cannot be empty")
            return False

        if not re.match(r"^[0-9x\+\-\*/\^ \(\)log10sqrt\.]+$", func_str.replace('**', '^').replace(' ', '')):
            self.show_error("Function contains invalid characters")
            return False

        try:
            float(min_x_str)
            float(max_x_str)
        except ValueError:
            self.show_error("Min and Max values must be valid numbers")
            return False

        return True

    def convert_function(self, func_str, x):
        """Convert the user-entered function string to a valid Python expression."""
        func_str = func_str.replace('^', '**')
        func_str = re.sub(r'log10\(([^)]+)\)', r'np.log10(\1)', func_str)
        func_str = re.sub(r'sqrt\(([^)]+)\)', r'np.sqrt(\1)', func_str)
        return func_str

    def show_error(self, message):
        """Display an error message to the user."""
        self.status_bar.showMessage(message, 5000)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())

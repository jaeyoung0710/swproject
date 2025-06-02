import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Engineering Calculator")
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(430, 900)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 42px; color: white; background-color: black; border: none;")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80)
        main_layout.addWidget(self.display)

        # Scientific buttons (6 x 5)
        sci_buttons = [
            ["(", ")", "mc", "m+", "m-"],
            ["2ⁿᵈ", "x²", "x³", "xʸ", "eˣ"],
            ["⅟x", "²√x", "³√x", "ʸ√x", "ln"],
            ["x!", "sin", "cos", "tan", "e"],
            ["Rand", "sinh", "cosh", "tanh", "π"],
            ["⌫", "+/-", "%", "Deg", "EE"]
        ]

        sci_grid = QGridLayout()
        for r, row in enumerate(sci_buttons):
            for c, label in enumerate(row):
                btn = QPushButton(label)
                btn.clicked.connect(self.on_click)
                btn.setStyleSheet(self.button_style(label, is_sci=True))
                btn.setFixedSize(75, 60)
                sci_grid.addWidget(btn, r, c)
        main_layout.addLayout(sci_grid)

        # Numeric/Operator buttons (5 x 4)
        calc_buttons = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["📱", "0", ".", "+"],
            ["", "", "", "="]
        ]

        calc_grid = QGridLayout()
        for r, row in enumerate(calc_buttons):
            for c, label in enumerate(row):
                if label == "":
                    continue
                btn = QPushButton(label)
                btn.clicked.connect(self.on_click)
                btn.setStyleSheet(self.button_style(label))
                btn.setFixedSize(90, 70)
                calc_grid.addWidget(btn, r, c)
        main_layout.addLayout(calc_grid)

        self.setLayout(main_layout)

    def button_style(self, label, is_sci=False):
        if label in {"=", "+", "-", "×", "÷"}:
            return "font-size: 22px; background-color: orange; color: white; border-radius: 30px;"
        elif label in {"⌫", "+/-", "%"}:
            return "font-size: 20px; background-color: #666666; color: white; border-radius: 30px;"
        elif is_sci:
            return "font-size: 16px; background-color: #222222; color: white; border-radius: 25px;"
        else:
            return "font-size: 22px; background-color: #333333; color: white; border-radius: 30px;"

    def on_click(self):
        sender = self.sender()
        current = self.display.text()
        self.display.setText(current + sender.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec_())

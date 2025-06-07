from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys, math, random

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone-Style Scientific Calculator")
        self.setStyleSheet("background-color: black;")
        self.init_ui()
        self.expression = ""
        self.memory = 0

    def init_ui(self):
        self.display = QLineEdit("0")
        self.display.setFont(QFont("Arial", 40))
        self.display.setStyleSheet("color: white; background-color: black; border: none;")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        buttons = [
            ["mc", "m+", "m-", "mr", "AC", "±", "%", "÷"],
            ["2nd", "x²", "x³", "xʸ", "7", "8", "9", "×"],
            ["1/x", "√", "∛", "ʸ√x", "4", "5", "6", "-"],
            ["ln", "log", "x!", "EE", "1", "2", "3", "+"],
            ["Rad", "sin", "cos", "tan", "Rand", "0", ".", "="]
        ]

        orange = {"÷", "×", "-", "+", "="}
        light = {"AC", "±", "%"}
        gray = {"mc", "m+", "m-", "mr", "2nd", "x²", "x³", "xʸ", "1/x", "√", "∛", "ʸ√x", "ln", "log", "x!", "EE", "Rad", "sin", "cos", "tan", "Rand"}

        for row_idx, row in enumerate(buttons):
            for col_idx, label in enumerate(row):
                span = 2 if label == "0" else 1
                btn = QPushButton(label)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                grid_layout.addWidget(btn, row_idx, col_idx, 1, span)

                if label in orange:
                    btn.setStyleSheet("background-color: #ff9500; color: white; font-size: 20pt;")
                elif label in light:
                    btn.setStyleSheet("background-color: #a5a5a5; color: black; font-size: 20pt;")
                elif label in gray:
                    btn.setStyleSheet("background-color: #505050; color: white; font-size: 20pt;")
                else:
                    btn.setStyleSheet("background-color: #333333; color: white; font-size: 20pt;")

                btn.clicked.connect(lambda checked, t=label: self.on_click(t))

    def on_click(self, text):
        if text == "AC":
            self.expression = ""
            self.display.setText("0")
        elif text == "=":
            try:
                expr = self.expression.replace("÷", "/").replace("×", "*").replace("x²", "**2").replace("x³", "**3")
                result = eval(expr)
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display.setText(self.expression)
        elif text == "%":
            try:
                result = float(self.expression) / 100
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "mc":
            self.memory = 0
        elif text == "m+":
            try:
                self.memory += float(self.display.text())
            except:
                pass
        elif text == "m-":
            try:
                self.memory -= float(self.display.text())
            except:
                pass
        elif text == "mr":
            self.expression = str(self.memory)
            self.display.setText(self.expression)
        elif text == "x!":
            try:
                result = math.factorial(int(float(self.display.text())))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "1/x":
            try:
                result = 1 / float(self.display.text())
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "√":
            try:
                result = math.sqrt(float(self.display.text()))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "∛":
            try:
                result = float(self.display.text()) ** (1/3)
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "ln":
            try:
                result = math.log(float(self.display.text()))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "log":
            try:
                result = math.log10(float(self.display.text()))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "sin":
            try:
                result = math.sin(math.radians(float(self.display.text())))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "cos":
            try:
                result = math.cos(math.radians(float(self.display.text())))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "tan":
            try:
                result = math.tan(math.radians(float(self.display.text())))
                self.expression = str(result)
                self.display.setText(self.expression)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "Rand":
            value = random.random()
            self.expression = str(value)
            self.display.setText(self.expression)
        else:
            self.expression += text
            self.display.setText(self.expression)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.resize(800, 400)
    calc.show()
    sys.exit(app.exec_())

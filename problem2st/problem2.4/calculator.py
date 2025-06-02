import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = "0"
        self.operator = None
        self.operand = None
        self.result_displayed = False

    def input_number(self, num):
        if self.result_displayed:
            self.current = num
            self.result_displayed = False
        elif self.current == "0" and num != ".":
            self.current = num
        else:
            if num == "." and "." in self.current:
                return
            self.current += num

    def set_operator(self, op):
        if self.operator and self.operand is not None:
            self.equal()
        self.operand = float(self.current)
        self.operator = op
        self.result_displayed = True

    def add(self):
        return self.operand + float(self.current)

    def subtract(self):
        return self.operand - float(self.current)

    def multiply(self):
        return self.operand * float(self.current)

    def divide(self):
        if float(self.current) == 0:
            raise ZeroDivisionError
        return self.operand / float(self.current)

    def negative_positive(self):
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current

    def percent(self):
        self.current = str(float(self.current) / 100)

    def equal(self):
        try:
            if self.operator == "+":
                self.current = str(self.add())
            elif self.operator == "-":
                self.current = str(self.subtract())
            elif self.operator == "×":
                self.current = str(self.multiply())
            elif self.operator == "÷":
                self.current = str(self.divide())
            self.operator = None
            self.operand = None
            self.result_displayed = True
        except ZeroDivisionError:
            self.current = "Error"
        except Exception:
            self.current = "Error"

    def get_display(self):
        if "." in self.current:
            return self.current.rstrip("0").rstrip(".") if "." in self.current else self.current
        return self.current


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(360, 640)
        self.setStyleSheet("background-color: black;")
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 36px; color: white; background-color: black; border: none;")
        self.display.setFixedHeight(100)
        vbox.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ["⌫", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["C", "0", ".", "="]
        ]

        for row in range(5):
            for col in range(4):
                label = buttons[row][col]
                btn = QPushButton(label)
                btn.setFixedSize(80, 80)
                if label in ["÷", "×", "-", "+", "="]:
                    btn.setStyleSheet("color: white; background-color: orange; font-size: 22px; border-radius: 40px;")
                elif label in ["⌫", "+/-", "%", "C"]:
                    btn.setStyleSheet("color: black; background-color: lightgray; font-size: 20px; border-radius: 40px;")
                else:
                    btn.setStyleSheet("color: white; background-color: #333333; font-size: 22px; border-radius: 40px;")
                btn.clicked.connect(self.handle_input)
                grid.addWidget(btn, row, col)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def handle_input(self):
        text = self.sender().text()
        if text.isdigit() or text == ".":
            self.calc.input_number(text)
        elif text == "+":
            self.calc.set_operator("+")
        elif text == "-":
            self.calc.set_operator("-")
        elif text == "×":
            self.calc.set_operator("×")
        elif text == "÷":
            self.calc.set_operator("÷")
        elif text == "=":
            self.calc.equal()
        elif text == "⌫":
            self.calc.current = self.calc.current[:-1] if self.calc.current != "0" else "0"
            if not self.calc.current:
                self.calc.current = "0"
        elif text == "+/-":
            self.calc.negative_positive()
        elif text == "%":
            self.calc.percent()
        elif text == "C":
            self.calc.reset()

        self.display.setText(self.calc.get_display())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CalculatorUI()
    win.show()
    sys.exit(app.exec_())

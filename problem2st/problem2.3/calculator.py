import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Calculator")
        self.setFixedSize(360, 600)
        self.createUI()

    def createUI(self):
        # 메인 레이아웃
        layout = QVBoxLayout()

        # 디스플레이
        self.display = QLabel("")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("font-size: 40px; background: black; color: white; padding: 20px;")
        layout.addWidget(self.display)

        # 버튼 레이아웃
        buttonLayout = QGridLayout()
        buttons = [
            ('⌫', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('📱', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 80)
            button.setStyleSheet("font-size: 24px;")
            button.clicked.connect(self.on_button_clicked)
            buttonLayout.addWidget(button, row, col)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def on_button_clicked(self):
        text = self.sender().text()
        if text == '⌫':
            self.display.setText(self.display.text()[:-1])
        elif text in ['=', '+', '-', '×', '÷', '%', '+/-', '📱']:
            pass  # 연산 기능 없음
        else:
            self.display.setText(self.display.text() + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

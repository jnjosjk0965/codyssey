import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(400, 600)
        self._result = "0"  # 현재 입력 또는 계산 결과
        self._num1 = "0"    # 첫 번째 숫자
        self._num2 = "0"    # 두 번째 숫자
        self._operator = "" # 연산자
        self._display_text = ""  # 디스플레이에 표시할 수식
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Display
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Arial", 36))
        self.display.setStyleSheet("background-color: black; color: white; border: none; padding: 10px;")
        self.display.setMinimumWidth(350)
        layout.addWidget(self.display, 0, 0, 1, 4)

        # Buttons
        buttons = [
            ("AC", 1, 0, "lightgray"), ("±", 1, 1, "lightgray"), ("%", 1, 2, "lightgray"), ("÷", 1, 3, "orange"),
            ("7", 2, 0, "darkgray"), ("8", 2, 1, "darkgray"), ("9", 2, 2, "darkgray"), ("×", 2, 3, "orange"),
            ("4", 3, 0, "darkgray"), ("5", 3, 1, "darkgray"), ("6", 3, 2, "darkgray"), ("−", 3, 3, "orange"),
            ("1", 4, 0, "darkgray"), ("2", 4, 1, "darkgray"), ("3", 4, 2, "darkgray"), ("+", 4, 3, "orange"),
            ("0", 5, 0, "darkgray", 2), (".", 5, 2, "darkgray"), ("=", 5, 3, "orange")
        ]

        for btn in buttons:
            text, row, col, color = btn[:4]
            colspan = btn[4] if len(btn) > 4 else 1
            button = QPushButton(text)
            button.setFont(QFont("Arial", 20))
            button.setStyleSheet(f"""
                QPushButton {{ 
                    background-color: {color}; 
                    color: {'white' if color != 'lightgray' else 'black'}; 
                    border-radius: {'30%' if text != '0' else '25%'}; 
                    border: none; 
                    padding: 20px;
                }}
                QPushButton:pressed {{ 
                    background-color: {'#b0b0b0' if color == 'lightgray' else '#505050' if color == 'darkgray' else '#ff9500'};
                }}
            """)
            button.clicked.connect(lambda _, t=text: self.calculate(t))
            layout.addWidget(button, row, col, 1, colspan)

        layout.setSpacing(10)
        self.setStyleSheet("background-color: black;")

    def update_display_text(self, text):
        length = len(text)
        if length <= 16:
            font_size = 36
        elif length <= 22:
            font_size = 28
        elif length <= 28:
            font_size = 22
        else:
            font_size = 18

        self.display.setFont(QFont("Arial", font_size))
        self.display.setText(text)

    def calculate(self, button_text):
        if button_text == "AC":
            self._reset()
        elif button_text == "±":
            self._negative_positive()
        elif button_text in ["+", "−", "×", "÷", "%"]:
            self._perform_operator(button_text)
        elif button_text == "=":
            self._equal()
        elif button_text == ".":
            self._perform_decimal_point()
        else:
            self._perform_input_number(button_text)
        self.update_display_text(self._display_text if self._display_text else self._result)

    def _reset(self):
        self._result = "0"
        self._num1 = "0"
        self._num2 = "0"
        self._operator = ""
        self._display_text = ""

    def _negative_positive(self):
        if self._result == "0":
            return
        if self._result.startswith("-"):
            self._result = self._result[1:]
        else:
            self._result = "-" + self._result
        if self._operator:
            self._num2 = self._result
            self._display_text = f"{self._num1} {self._operator} {self._result}"
        else:
            self._num1 = self._result
            self._display_text = self._result

    def _perform_operator(self, operator):
        if self._operator and self._num2 != "0":
            # 이전 연산 수행
            try:
                num1 = float(self._num1)
                num2 = float(self._num2)
                if self._operator == "+":
                    result = num1 + num2
                elif self._operator == "−":
                    result = num1 - num2
                elif self._operator == "×":
                    result = num1 * num2
                elif self._operator == "÷":
                    if num2 == 0:
                        self._result = "Error"
                        self._display_text = "Error"
                        return
                    result = num1 / num2
                elif self._operator == "%":
                    if num2 == 0:
                        self._result = "Error"
                        self._display_text = "Error"
                        return
                    result = num1 % num2
                result = round(result, 6)
                self._num1 = str(result).rstrip(".0") if result.is_integer() else str(result)
                self._result = "0"
                self._num2 = "0"
            except:
                self._result = "Error"
                self._display_text = "Error"
                return
        else:
            self._num1 = self._result
            self._result = "0"
        self._operator = operator
        self._display_text = f"{self._num1} {operator} "

    def _equal(self):
        try:
            number = float(self._result)
            if self._operator:
                num1 = float(self._num1)
                num2 = float(self._num2 if self._num2 != "0" else self._result)
                if self._operator == "+":
                    number = self._add(num1, num2)
                elif self._operator == "−":
                    number = self._subtract(num1, num2)
                elif self._operator == "×":
                    number = self._multiply(num1, num2)
                elif self._operator == "÷":
                    number = self._divide(num1, num2)
                elif self._operator == "%":
                    number = self._percent(num1, num2)
            number = round(number, 6)
            self._result = str(number).rstrip(".0") if number.is_integer() else str(number)
            self._num1 = self._result
            self._num2 = "0"
            self._operator = ""
            self._display_text = self._result
        except:
            self._result = "Error"
            self._display_text = "Error"

    def _perform_decimal_point(self):
        if "." in self._result:
            return
        self._result = self._result + "."
        if self._operator:
            self._num2 = self._result
            self._display_text = f"{self._num1} {self._operator} {self._result}"
        else:
            self._num1 = self._result
            self._display_text = self._result

    def _perform_input_number(self, number):
        self._result = number if self._result == "0" else self._result + number
        if self._operator:
            self._num2 = self._result
            self._display_text = f"{self._num1} {self._operator} {self._result}"
        else:
            self._num1 = self._result
            self._display_text = self._result

    def _add(self, a, b):
        return a + b
    def _subtract(self, a, b):
        return a - b
    def _multiply(self, a, b):
        return a * b
    def _divide(self, a, b):
        if b == 0:
            self._result = "Error"
            self._display_text = "Error"
            return None
        return a / b
    def _percent(self, a, b):
        if b == 0:
            self._result = "Error"
            self._display_text = "Error"
            return None
        return a % b

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
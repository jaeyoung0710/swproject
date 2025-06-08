import math

class Calculator:
    def __init__(self):
        self.memory = 0.0

    def add(self, x, y): return x + y
    def subtract(self, x, y): return x - y
    def multiply(self, x, y): return x * y
    def divide(self, x, y):
        if y == 0:
            raise ZeroDivisionError("0À¸¸ 나누는 수 없습니다.")
        return x / y

class EngineeringCalculator(Calculator):
    def square(self, x):
        return x ** 2

    def cube(self, x):
        return x ** 3

    def power(self, x, y):
        return x ** y

    def exp(self, x):
        return math.exp(x)

    def ten_power(self, x):
        return 10 ** x

    def sqrt(self, x):
        if x < 0:
            raise ValueError("음수의 제공률은 정의되지 않습니다.")
        return math.sqrt(x)

    def cbrt(self, x):
        return x ** (1.0 / 3.0)

    def y_root(self, x, y):
        if y == 0:
            raise ZeroDivisionError("0À¸¸ 루트를 계산할 수 없습니다.")
        return x ** (1.0 / y)

    def reciprocal(self, x):
        if x == 0:
            raise ZeroDivisionError("0의 역수는 정의되지 않습니다.")
        return 1 / x

    def ln(self, x):
        if x <= 0:
            raise ValueError("자연 로그는 0 이하에서 정의되지 않습니다.")
        return math.log(x)

    def log10(self, x):
        if x <= 0:
            raise ValueError("상용 로그는 0 이하에서 정의되지 않습니다.")
        return math.log10(x)

    def factorial(self, x):
        if x < 0 or not float(x).is_integer():
            raise ValueError("팩토리앙은 0 이상의 정수에서만 정의됩니다.")
        return math.factorial(int(x))

    def rand(self):
        import random
        return random.random()

    def calculate_sin(self, x): return math.sin(x)
    def calculate_cos(self, x): return math.cos(x)
    def calculate_tan(self, x): return math.tan(x)

    def calculate_sinh(self, x): return math.sinh(x)
    def calculate_cosh(self, x): return math.cosh(x)
    def calculate_tanh(self, x): return math.tanh(x)

    def get_pi(self): return math.pi
    def get_e(self): return math.e

    def deg_to_rad(self, deg): return math.radians(deg)
    def rad_to_deg(self, rad): return math.degrees(rad)

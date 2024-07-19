from jose import jwt
import pytest

token = None

# def test_token():
#     token = jwt.encode({'key': 'value'}, 'secret', algorithm='HS256')
#     print(token)

# def test_token_decode():
#     data = jwt.decode(token, 'secret', algorithms=['HS256'])
#     print(data)


class Calculator():
    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y

    def div(self, x, y):
        return x / y

def test_add():
    calculator = Calculator()
    assert calculator.add(1, 2) == 3
    assert calculator.add(2, 2) == 4


def test_sub():
    calculator = Calculator()
    assert calculator.sub(5, 1) == 4
    assert calculator.sub(3, 2) == 1

def test_mul():
    calculator = Calculator()
    assert calculator.mul(2, 2) == 4
    assert calculator.mul(5, 6) == 30

def test_div():
    calculator = Calculator()
    assert calculator.div(8, 2) == 4
    assert calculator.div(9, 3) == 3


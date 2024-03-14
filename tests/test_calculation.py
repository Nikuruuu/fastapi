import pytest
from app.calculation import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (10, 10, 20),
    (9, 4, 13)
])
def test_add(num1, num2, result):
    assert add(num1, num2) == result


# def test_subtract():
#     assert subtract (9, 4) == 5

# def test_multiply():
#     assert multiply (9, 4) == 36

# def test_divide():
#     assert divide (8, 4) == 2

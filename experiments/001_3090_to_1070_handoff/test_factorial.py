import pytest
from factorial import factorial

def test_factorial_zero():
    """Test factorial of 0"""
    assert factorial(0) == 1

def test_factorial_one():
    """Test factorial of 1"""
    assert factorial(1) == 1

def test_factorial_five():
    """Test factorial of 5"""
    assert factorial(5) == 120

def test_factorial_ten():
    """Test factorial of 10"""
    assert factorial(10) == 3628800

def test_factorial_negative():
    """Test that negative input raises ValueError"""
    with pytest.raises(ValueError):
        factorial(-1)
        
def test_factorial_negative_large():
    """Test that large negative input raises ValueError"""
    with pytest.raises(ValueError):
        factorial(-5)
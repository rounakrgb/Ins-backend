import pytest

def divide(x,y):
    if y == 0:
        raise ValueError("Cannot divide by 0")
    
    return x/y

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by 0"):
        divide(5,0)

divide(4,9)
test_divide_by_zero()


def f():
    return 4  

def test_function():
    assert f() == 4
        
f()
test_function()        


import numpy as np

def test_floats():
    a = np.array([1.0,2.0,3.0])
    b = np.array([0.00001,2.0001,3.0])
    assert a == pytest.approx(b)
    
test_floats    
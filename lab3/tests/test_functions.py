import math

from lab3.serializer.helpers.Converter import convert, deconvert


# from lab3.serializer.JSONSerializer import JSONSerializer
# ser = JSONSerializer()
# convert = ser.dumps
# deconvert = ser.loads

# from lab3.serializer.XMLSerializer import XMLSerializer
# ser = XMLSerializer()
# convert = ser.dumps
# deconvert = ser.loads

def simple_func(name):
    return "hello " + name

def test_simple():
    assert deconvert(convert(simple_func))("anna") == simple_func("anna")


a = 3
def with_global_func(b):
    return a + b

def test_global():
    assert deconvert(convert(with_global_func))(5) == with_global_func(5)

def with_defaults_func(x=1, y=2):
    return x + y

def test_defaults():
    assert deconvert(convert(with_defaults_func))(3) == with_defaults_func(3)


def recursive_func(val):
    if val == 1:
        return 1
    return recursive_func(val-1) + val

def test_recursive():
    assert deconvert(convert(recursive_func))(10) == recursive_func(10)


def nested_func():
    var = "hello"
    def inner():
        return var
    return inner

def test_nested():
    assert deconvert(convert(nested_func))()() == nested_func()()


def func_in_func():
    val = "anna"
    return simple_func("anna")

def test_nested2():
    assert deconvert(convert(func_in_func))() == func_in_func()


def with_imported_func(x):
    return math.sin(x) % 100 + 5

def test_with_imported():
    assert deconvert(convert(with_imported_func))(2) == with_imported_func(2)

l = lambda x: x**2

def test_lambda():
    assert deconvert(convert(l))(5) == l(5)

def lambda_nested_func():
    b = 3
    return lambda c: c * b

def test_lambda2():
    assert deconvert(convert(lambda_nested_func))()(5) == lambda_nested_func()(5)

def wrapper(func):
    return func("hello")

def test_wrapper():
    assert deconvert(convert(wrapper))(simple_func) == wrapper(simple_func)

def decorator(func):
    def wrapper():
        return func() + 10
    return wrapper

@decorator
def fun():
    return 5

def test_decorator():
    assert deconvert(convert(fun))() == fun()

def with_builtin(s):
    return len(s)

def test_builtins():
    assert deconvert(convert(with_builtin))("hello") == with_builtin("hello")

def test_generator():
    a = (i ** 2 for i in range(1, 5))
    b = deconvert(convert(a))
    assert [1, 4, 9, 16] == [x for x in b]
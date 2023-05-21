from lab3.serializer.helpers.Converter import convert, deconvert


# from lab3.serializer.JSONSerializer import JSONSerializer
# ser = JSONSerializer()
# convert = ser.dumps
# deconvert = ser.loads

# from lab3.serializer.XMLSerializer import XMLSerializer
# ser = XMLSerializer()
# convert = ser.dumps
# deconvert = ser.loads
class A:
    var1 = "class var"

    def __init__(self, x):
        self.var2 = x
        self.var3 = 8

    def sum(self):
        return self.var2 + self.var3

    @classmethod
    def class_func(cls):
        return cls.var1


class B:
    def __init__(self, x, y):
        self.var4 = x
        self.var5 = y

    def sum(self):
        return self.var4 - self.var5

    def div(self, divisor):
        return self.var4 / divisor

    def pow(self):
        return self.var5 ** 2

    @staticmethod
    def get_number():
        return 10


class C(A, B):
    def __init__(self, a, b, c):
        A.__init__(self, a)
        B.__init__(self, b, c)

    def pow(self):
        return self.var5 ** 3


rebuild_A = deconvert(convert(A))
rebuild_B = deconvert(convert(B))
rebuild_C = deconvert(convert(C))

a = A(3)
b = B(10, 15)
c = C(7, 8, 15)

rebuild_a = deconvert(convert(a))
rebuild_b = deconvert(convert(b))
rebuild_c = deconvert(convert(c))


def test_classmethod():
    assert rebuild_A.class_func() == A.class_func()


def test_staticmethod():
    assert rebuild_B.get_number() == B.get_number()


def test_inheritance_class():
    assert rebuild_C.class_func() == C.class_func()


def test_inheritance_static():
    assert rebuild_C.get_number() == C.get_number()


def test_inheritance_class1():
    assert rebuild_C.var1 == C.var1


def test_inheritance1():
    assert rebuild_c.sum() == c.sum()


def test_inheritance2():
    assert rebuild_c.div(2) == c.div(2)


def test_override1():
    assert rebuild_c.pow() == c.pow()


def test_override2():
    assert rebuild_c.pow() != b.pow()


def test_init():
    var = rebuild_C(7, 8, 15)
    assert var.sum() == c.sum()


class ClassWithProperty:
    a = 1

    @property
    def test_prop(self):
        return self.a


def test_property():
    rebuild = deconvert(convert(ClassWithProperty()))
    assert rebuild.test_prop == ClassWithProperty().test_prop



def test_metaclass1():
    class MyType(type):
        def __new__(cls, name, bases, dct):
            x = super().__new__(cls, name, bases, dct)
            x.attr = 100
            return x

    T = deconvert(convert(MyType))

    class X(metaclass=T):
        pass

    a = X()
    assert a.attr == 100
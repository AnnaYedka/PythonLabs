from lab3.serializer.helpers.Converter import convert, deconvert

# from lab3.serializer.JSONSerializer import JSONSerializer
# ser = JSONSerializer()
# convert = ser.dumps
# deconvert = ser.loads

# from lab3.serializer.XMLSerializer import XMLSerializer
# ser = XMLSerializer()
# convert = ser.dumps
# deconvert = ser.loads

def test_int():
    val = 12
    assert deconvert(convert(val)) == val


def test_float():
    val = 12.43
    assert deconvert(convert(val)) == val


def test_str():
    val = "hello"
    assert deconvert(convert(val)) == val


def test_bool():
    val = True
    assert deconvert(convert(val)) == val


def test_list():
    val = [1, 3, "str"]
    assert deconvert(convert(val)) == tuple(val)


def test_set():
    val = {1.3, 4, "hsj"}
    assert deconvert(convert(val)) == tuple(val)


def test_tuple():
    val = 1, 4, "sdg"
    assert deconvert(convert(val)) == val


def test_dict():
    val = {1: "1", 2: "2", 3: "3"}
    assert deconvert(convert(val)) == val


def test_nested():
    val = {1: (1, 3, 4), 2: "hjk", 3: {1: "1", 2: "2"}}
    assert deconvert(convert(val)) == val

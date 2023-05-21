import builtins
import collections.abc
import inspect
from types import FunctionType, CodeType, ModuleType, MethodType, CellType, BuiltinMethodType, BuiltinFunctionType

from .consts import PRIMITIVE_TYPES, ITERABLE_TYPES, NOT_SERIALIZABLE, NOT_SERIALIZABLE_TYPES


def convert(obj):
    if type(obj) in PRIMITIVE_TYPES:
        return obj
    elif type(obj) in ITERABLE_TYPES:
        return _convert_iterable(obj)

    elif type(obj) == dict:
        return _convert_dict(obj)
    elif isinstance(obj, type):
        return _convert_class(obj)
    elif isinstance(obj, (MethodType, FunctionType)):
        return _convert_func(obj)
    elif isinstance(obj, (BuiltinFunctionType, BuiltinMethodType)):
        return {}
    elif isinstance(obj, classmethod):
        return {"classmethod": _convert_func(obj.__func__)}
    elif isinstance(obj, staticmethod):
        return {"staticmethod": _convert_func(obj.__func__)}
    elif isinstance(obj, CodeType):
        return {"code": _convert_code(obj)}
    elif isinstance(obj, ModuleType):
        return {"module": obj.__name__}
    elif isinstance(obj, collections.abc.Iterator):
        return {"iterator": _convert_iterable(list(obj))}
    else:
        return _convert_instance(obj)


def _convert_iterable(obj):
    tmp = []
    for val in obj:
        tmp.append(convert(val))
    return tuple(tmp)


def _convert_dict(obj: dict) -> dict:
    tmp = {}
    for key, value in obj.items():
        tmp[convert(key)] = convert(value)
    return tmp


def _convert_class(obj) -> dict:
    if obj.__bases__[0] == object:
        bases = ()
    elif obj.__bases__[0] == type:
        bases = ('type',)
    else:
        bases = obj.__bases__

    tmp = {"name": obj.__name__,
           "bases": bases,
           "attr": {key: value for key, value in obj.__dict__.items()
                    if key not in NOT_SERIALIZABLE and type(value) not in NOT_SERIALIZABLE_TYPES}}
    return {"class": _convert_dict(tmp)}


def _convert_instance(obj) -> dict:
    try:
        attr = {key: value for key, value in obj.__dict__.items()
                if key not in NOT_SERIALIZABLE}
    except AttributeError:
        attr = {key: value for key, value in inspect.getmembers(obj)
                if key not in NOT_SERIALIZABLE and not key.startswith("__") and type(value) not in NOT_SERIALIZABLE_TYPES}
    tmp = {"class": obj.__class__,
           "attr": attr}
    return {"instance": _convert_dict(tmp)}


def _convert_func(obj: FunctionType) -> dict:
    if obj.__closure__ is None:
        closure = ()
    else:
        clas = obj.__qualname__.split("<locals>.")[-1].rsplit(".", 1)[0]
        closure = []
        for cell in obj.__closure__:
            if cell.cell_contents.__name__ == clas:
                closure.append(None)
            else:
                closure.append(cell.cell_contents)
    tmp = {"code": _convert_code(obj.__code__),
           "globals": _get_globals(obj),
           "name": obj.__name__,
           "argdefs": obj.__defaults__,
           "closure": tuple(closure)
           }
    return {"function": _convert_dict(tmp)}


def _convert_code(obj: CodeType) -> dict:
    tmp = {
        "argcount": obj.co_argcount,
        "posonlyargcount": obj.co_posonlyargcount,
        "kwonlyargcount": obj.co_kwonlyargcount,
        "nlocals": obj.co_nlocals,
        "stacksize": obj.co_stacksize,
        "flags": obj.co_flags,
        "codestring": obj.co_code.hex(),
        "constants": obj.co_consts,
        "names": obj.co_names,
        "varnames": obj.co_varnames,
        "filename": obj.co_filename,
        "name": obj.co_name,
        "firstlineno": obj.co_firstlineno,
        "lnotab": obj.co_lnotab.hex(),
        "freevars": obj.co_freevars,
        "cellvars": obj.co_cellvars
    }
    return _convert_dict(tmp)


def _get_globals(func: FunctionType) -> dict:
    tmp = {}
    clas = func.__qualname__.rsplit(".", 1)[0]
    for var in func.__code__.co_names:
        if var in func.__globals__.keys() and var != func.__name__ and var != clas:
            tmp[var] = func.__globals__[var]
    return tmp


def deconvert(obj: dict):
    if type(obj) in PRIMITIVE_TYPES:
        return obj
    elif type(obj) == tuple:
        obj = list(obj)
        return tuple([deconvert(val) for val in obj])
    elif not obj:
        return {}

    if type(obj) != dict:
        return obj

    obj_type = list(obj.keys())[0]
    if obj_type == "class":
        return _deconvert_class(obj[obj_type])
    if obj_type == "function":
        return _deconvert_func(obj[obj_type])
    if obj_type == "instance":
        return _deconvert_instance(obj[obj_type])
    if obj_type == "code":
        return _deconvert_code(obj[obj_type])
    if obj_type == "staticmethod":
        return staticmethod(deconvert(obj[obj_type]))
    if obj_type == "classmethod":
        return classmethod(deconvert(obj[obj_type]))
    if obj_type == "module":
        return __import__(obj[obj_type])
    if obj_type == "iterator":
        return iter(deconvert(obj[obj_type]))
    return _deconvert_dict(obj)


def _deconvert_dict(obj: dict):
    tmp = {}
    for key, value in obj.items():
        tmp[deconvert(key)] = deconvert(value)
    return tmp


def _deconvert_func(obj: dict, cls=None):
    func_dict = _deconvert_dict(obj)
    c: CodeType = _deconvert_code(func_dict["code"])
    if cls:
        closure = (CellType(cls),)
    else:
        closure = tuple([CellType(val) for val in func_dict["closure"]])
    if func_dict["argdefs"] is None:
        defs = ()
    else:
        defs = (tuple(func_dict["argdefs"]))

    # add built-in functions to globals
    globals = func_dict["globals"]
    for val in c.co_names:
        if val in builtins.__dict__.keys():
            globals.update({val: builtins.__dict__[val]})

    func = FunctionType(code=c,
                        globals=globals,
                        name=func_dict["name"],
                        argdefs=defs,
                        closure=closure
                        )
    func.__globals__.update({func.__name__: func})
    return func


def _deconvert_class(obj: dict):

    if obj["bases"] and obj["bases"][0] == 'type':
        meta = type(obj["name"], (type,), {})
        for key, val in obj["attr"].items():
            if key == "__module__" or key == "__doc__":
                setattr(meta, f"{key}", deconvert(val))
            else:
                while key != "function":
                    key, val = list(val.items())[0]
                deconverted_func = _deconvert_func(val, meta)
                setattr(meta, f"{deconverted_func.__name__}", deconverted_func)
        return meta

    class_dict = _deconvert_dict(obj)
    if class_dict["bases"]:
        bases = tuple(class_dict["bases"])
    else:
        bases = (object,)
    return type(class_dict["name"], bases, class_dict["attr"])


def _deconvert_instance(obj: dict):
    instance_dict = _deconvert_dict(obj)
    instance_class = instance_dict["class"]
    if instance_class.__name__ == 'property':
        return property(instance_dict['attr']["fget"], instance_dict['attr']["fset"], instance_dict['attr']["fdel"])
    instance = object.__new__(instance_class)
    instance.__dict__ = instance_dict["attr"]
    return instance


def _deconvert_code(obj: dict):
    code_dict = _deconvert_dict(obj)
    return CodeType(code_dict["argcount"],
                    code_dict["posonlyargcount"],
                    code_dict["kwonlyargcount"],
                    code_dict["nlocals"],
                    code_dict["stacksize"],
                    code_dict["flags"],
                    bytes.fromhex(code_dict["codestring"]),
                    tuple(code_dict["constants"]),
                    tuple(code_dict["names"]),
                    tuple(code_dict["varnames"]),
                    code_dict["filename"],
                    code_dict["name"],
                    code_dict["firstlineno"],
                    bytes.fromhex(code_dict["lnotab"]),
                    tuple(code_dict["freevars"]),
                    tuple(code_dict["cellvars"]))

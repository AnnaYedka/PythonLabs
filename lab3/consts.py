from types import NoneType

PRIMITIVE_TYPES = (int, float, complex, str, bool, NoneType)
ITERABLE_TYPES = (list, set, tuple)
NOT_SERIALIZABLE = ('__weakref__', '__dict__')

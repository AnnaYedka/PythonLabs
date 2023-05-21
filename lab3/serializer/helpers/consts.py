import types
PRIMITIVE_TYPES = (int, float, complex, str, bool, type(None))
ITERABLE_TYPES = (list, set, tuple)
NOT_SERIALIZABLE = ('__weakref__', '__dict__', '__class__')
NOT_SERIALIZABLE_TYPES = [
    types.WrapperDescriptorType, types.MethodDescriptorType,
    types.BuiltinFunctionType, types.MappingProxyType,
    types.GetSetDescriptorType, types.MethodWrapperType,
    types.MemberDescriptorType
]
JSON_STYLE_VALUES = {True: "true", False: "false", None: "null"}

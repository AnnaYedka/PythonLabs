from serializer import Serializer
from consts import JSON_STYLE_VALUES


class JSONSerializer(Serializer):
    def dump(self, obj, fp):
        pass

    def dumps(self, obj) -> str:
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass


    def _serialize(self, obj, indent=0) -> str:
        if type(obj) == dict:
            if not obj:
                return "{}"
            tmp = "{"
            for key in list(obj)[:-1]:
                tmp += ",\n" + "    " * indent + self._serialize(key) + ": " + self._serialize(obj[key], indent + 1)
            return tmp + self._serialize(list(obj)[-1]) + ": " + self._serialize(obj[list(obj)[-1]], indent + 1) + "\n" + "    "*indent + "}"

        if type(obj) == str:
            return f'"{obj}"'
        if type(obj) in (int, float, complex):
            return str(obj)
        if type(obj) == list:
            if not obj:
                return "[]"
            tmp = "["
            for item in obj[:-1]:
                tmp += self._serialize(item) + ", "
            return tmp + self._serialize(obj[-1]) + "]"

        if obj in JSON_STYLE_VALUES.keys():
            return JSON_STYLE_VALUES[obj]

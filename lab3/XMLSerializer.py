from serializer import Serializer
from consts import PRIMITIVE_TYPES, ITERABLE_TYPES
from Converter import convert, deconvert

class XMLSerializer(Serializer):
    def dump(self, obj, fp):
        with open(fp, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        return self._serialize(convert(obj))

    def load(self, fp):
        with open(fp, "r") as file:
            return self.loads(file.read())

    def loads(self, s: str):
        pass

    def _serialize(self, obj, indent=0) -> str:
        t = type(obj)
        if t in PRIMITIVE_TYPES:
            return str(obj)
        if t in ITERABLE_TYPES:
            tmp = "\n"+"    "*indent + "<list>"
            for val in obj:
                if type(val) in PRIMITIVE_TYPES:
                    tmp += "\n"+"    "*(indent+1) + "<item>" + self._serialize(val, indent+2) + "</item>"
                else:
                    tmp += "\n" + "    " * (indent + 1) + "<item>" + self._serialize(val, indent + 2) + \
                           "    " *(indent + 1) +"</item>"
            tmp += "\n"+"    "*indent + "</list>" + "\n"
            return tmp

        tmp = ""
        for k, v in obj.items():
            if type(v) in PRIMITIVE_TYPES:
                tmp += "\n" + "    " * indent + f"<{self._serialize(k, indent + 1)}>{self._serialize(v, indent + 1)}" +\
                        f"</{self._serialize(k, indent + 1)}>"
            else:
                tmp += "\n"+"    "*indent + f"<{self._serialize(k, indent+1)}>{self._serialize(v, indent+1)}" +\
                   "    "*indent + f"</{self._serialize(k, indent+1)}>"
        return tmp + "\n"


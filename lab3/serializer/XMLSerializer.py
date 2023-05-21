import re

from .helpers.Converter import convert, deconvert
from .helpers.consts import PRIMITIVE_TYPES, ITERABLE_TYPES


class XMLSerializer:
    def dump(self, obj, fp):
        with open(fp, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        return self._serialize(convert(obj))

    def load(self, fp):
        with open(fp, "r") as file:
            return self.loads(file.read())

    def loads(self, s: str):
        s = s.replace("\n", "")
        s = s.replace("    ", "")
        return deconvert(self._deserialize(s)[0])

    def _serialize(self, obj, indent=0) -> str:
        t = type(obj)
        if t == str:
            return f'"{obj}"'
        if t in PRIMITIVE_TYPES:
            return str(obj)
        if t in ITERABLE_TYPES:
            tmp = "\n" + "    " * indent + "<list>"
            for val in obj:
                if type(val) in PRIMITIVE_TYPES:
                    tmp += "\n" + "    " * (indent + 1) + "<item>" + self._serialize(val, indent + 2) + "</item>"
                else:
                    tmp += "\n" + "    " * (indent + 1) + "<item>" + self._serialize(val, indent + 2) + \
                           "    " * (indent + 1) + "</item>"
            tmp += "\n" + "    " * indent + "</list>" + "\n"
            return tmp

        tmp = "\n"
        for k, v in obj.items():
            if type(v) in PRIMITIVE_TYPES:
                tmp += "    " * indent + f"<{self._serialize(k, indent + 1)}>{self._serialize(v, indent + 1)}" + \
                       f"</{self._serialize(k, indent + 1)}>" + "\n"
            else:
                tmp += "    " * indent + f"<{self._serialize(k, indent + 1)}>{self._serialize(v, indent + 1)}" + \
                       "    " * indent + f"</{self._serialize(k, indent + 1)}>" + "\n"
        return tmp

    def _deserialize(self, s: str, i: int = 0):
        if s == "":
            return {}
        if s[i] != "<":
            return self._deserialize_primitive(s, i)
        elif len(s) - i > 5 and s[i:i + 6] == "<list>":
            return self._deserialize_list(s, i)
        else:
            return self._deserialize_dict(s, i)

    def _deserialize_dict(self, s: str, i: int):
        tmp = {}
        while i < len(s) and s[i + 1] != "/":
            length = i
            key, i = self._get_key(s, i)
            length = i - length
            val, i = self._deserialize(s, i)
            i += length + 1
            tmp.update({key: val})
        return tmp, i

    def _deserialize_list(self, s: str, i: int):
        open_brackets = 1
        i += 6
        end = i
        tmp = []
        while open_brackets:
            if s[end:end + 7] == "</list>":
                open_brackets -= 1
                end += 6
            elif s[end:end + 6] == "<list>":
                open_brackets += 1
                end += 5
            end += 1
        while i < end - 7:
            val, i = self._deserialize_list_item(s, i)
            tmp.append(val)
        return tuple(tmp), end

    def _deserialize_list_item(self, s: str, i: int):
        open_brackets = 1
        i += 6
        start = i
        while open_brackets:
            if s[i:i + 7] == "</item>":
                open_brackets -= 1
                i += 6
            elif s[i:i + 6] == "<item>":
                open_brackets += 1
                i += 6
            i += 1
        return self._deserialize(s, start)[0], i

    def _get_key(self, s: str, i: int):
        open_brackets = 1
        i += 1
        start = i
        while i < len(s) and open_brackets:
            if s[i] == "<":
                open_brackets += 1
            elif s[i] == ">":
                open_brackets -= 1
            i += 1
        return self._deserialize(s, start)[0], i

    def _deserialize_primitive(self, s: str, i: int):
        start = i
        if s[i] == "\"":
            i += 1
            while s[i] != "\"":
                i += 1
            return s[start+1:i], i + 1
        while i < len(s) and s[i] != "<" and s[i] != ">":
            i += 1
        val = s[start:i]
        if val == "None":
            return None, i
        if val == "True":
            return True, i
        if val == "False":
            return False, i
        if re.search(r"-?[0-9]+\.[0-9]+", val):
            return float(re.search(r"-?[0-9]+\.[0-9]+", val).group()), i
        if re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", val):
            return complex(re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", val).group()), i
        if re.search(r"-?[0-9]+", val):
            return int(re.search(r"[0-9]+", val).group()), i
        return val, i

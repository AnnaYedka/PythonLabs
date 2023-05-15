import re

from serializer import Serializer
from consts import JSON_STYLE_VALUES
from Converter import convert, deconvert


class JSONSerializer(Serializer):
    def dump(self, obj, fp):
        with open(fp, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        return self._serialize(convert(obj))

    def load(self, fp):
        with open(fp, "r") as file:
            return self.loads(file.read())

    def loads(self, s: str):
        return deconvert(self._deserialize(s))

    def _serialize(self, obj, indent=0) -> str:
        if type(obj) == dict:
            if not obj:
                return "{}"
            tmp = "{"
            for key in list(obj)[:-1]:
                tmp += "\n" + "    " * indent + self._serialize(key) + ": " + self._serialize(obj[key],
                                                                                              indent + 1) + ","
            return tmp + "\n" + "    " * indent + self._serialize(list(obj)[-1]) + ": " + \
                   self._serialize(obj[list(obj)[-1]], indent + 1) + "\n" + "    " * indent + "}"

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

    def _deserialize(self, s: str) -> dict:
        lines = s.split("\n")
        return self._deserialize_line(lines)

    def _deserialize_line(self, lines):
        j = 0
        if lines[j] == "{":
            j = 1
        tmp = {}

        while j < len(lines):
            line = lines[j]

            if re.search(r"\s*(.+): (.+)", line):
                match = re.search(r"\s*(.+): (.+)", line)
                key = match.group(1)
                val = match.group(2)
                j += 1
                if val == "{":
                    open_count = 0
                    close_count = 0
                    for i in range(j, len(lines)):
                        open_count += lines[i].count("{")
                        close_count += lines[i].count("}")
                        if close_count > open_count:
                            val = self._deserialize_line(lines[j:i+1])
                            j = i+1
                            break
                    tmp.update({self._deserialize_line([key]): val})
                else:
                    tmp.update({self._deserialize_line([key]): self._deserialize_line([val])})

            elif "}" in line:
                return tmp

            elif "[" in line:
                open_count = 0
                close_count = 0
                for i in range(j, len(lines)):
                    open_count += lines[i].count("[")
                    close_count += lines[i].count("]")
                    if close_count == open_count:
                        return self._deserialize_list("".join(lines[j:i+1]))
            else:
                return self._deserialize_primitive(line)

    def _deserialize_list(self, s: str):
        if s[-1] == ",":
            values = s[1:-2].split(", ")
        else:
            values = s[1:-1].split(", ")

        l = []
        for val in values:
            if val:
                l.append(self._deserialize_line([val]))
        return tuple(l)

    def _deserialize_primitive(self, s: str):
        if s == "null":
            return None
        if s == "true":
            return True
        if s == "false":
            return False
        if re.search(r"\"(.+)\"", s):
            return re.search(r"\"(.+)\"", s).group(1)
        if re.search(r"-?[0-9]+\.[0-9]+", s):
            return float(re.search(r"-?[0-9]+\.[0-9]+", s).group())
        if re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s):
            return complex(re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s).group())
        if re.search(r"-?[0-9]+", s):
            return int(re.search(r"[0-9]+", s).group())

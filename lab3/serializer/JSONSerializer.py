import re

from .helpers.Converter import convert, deconvert
from .helpers.consts import JSON_STYLE_VALUES


class JSONSerializer:
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
        return deconvert(self._deserialize(s))

    def _serialize(self, obj, indent=0) -> str:
        if type(obj) == dict:
            if not obj:
                return "{}"
            tmp = "{"
            for key in list(obj)[:-1]:
                tmp += "\n" + "    " * indent + self._serialize(key, indent+1) + ": " + self._serialize(obj[key],
                                                                                              indent + 1) + ","
            return tmp + "\n" + "    " * indent + self._serialize(list(obj)[-1], indent+1) + ": " + \
                   self._serialize(obj[list(obj)[-1]], indent + 1) + "\n" + "    " * indent + "}"

        if type(obj) == str:
            return f'"{obj}"'
        if type(obj) in (int, float, complex):
            return str(obj)
        if type(obj) == tuple:
            if not obj:
                return "[]"
            tmp = "["
            for item in obj[:-1]:
                tmp += self._serialize(item, indent+1) + ", "
            return tmp + self._serialize(obj[-1], indent+1) + "]"

        if obj in JSON_STYLE_VALUES.keys():
            return JSON_STYLE_VALUES[obj]

    def _deserialize(self, s: str):
        i = 0
        if s[i] == " ":
            i+=1
        if s[i] == "{":
            return self._deserialize_dict(s, i)[0]
        elif s[i] == "[":
            return self._deserialize_list(s, i)[0]
        else:
            return self._deserialize_primitive(s)
    def _deserialize_dict(self, s, i):
        tmp = {}
        i += 1
        open_count = 0
        close_count = 0
        key = ""
        val = ""
        update_key = True
        check_end = True
        while True:
            if check_end and s[i] == ":":
                update_key = False
                i += 1
            elif check_end and s[i] == ",":
                update_key = True
                if type(key) != str:
                    tmp.update({key: self._deserialize(val)})
                elif type(val) != str:
                    tmp.update({self._deserialize(key): val})
                else:
                    tmp.update({self._deserialize(key): self._deserialize(val)})
                key = ""
                val = ""
                i += 1
            if s[i] == "{":
                check_end = False
                open_count += 1
            elif s[i] == "}":
                close_count += 1

            elif s[i] == "[" and check_end:
                if update_key:
                    key, i = self._deserialize_list(s, i)
                else:
                    val, i = self._deserialize_list(s, i)
                continue

            if close_count and close_count == open_count:
                check_end = True
            if close_count > open_count:
                if type(key) != str:
                    tmp.update({key: self._deserialize(val)})
                elif type(val) != str:
                    tmp.update({self._deserialize(key): val})
                else:
                    if key == "":
                        i += 1
                        return tmp, i
                    tmp.update({self._deserialize(key): self._deserialize(val)})
                i+=1
                break

            if update_key:
                key += s[i]
            else:
                val += s[i]
            i += 1
        return tmp, i

    def _deserialize_list(self, s, i):
        tmp = []
        val = ""
        open_count = 0
        close_count = 0
        i += 1
        check_end = True
        while True:
            if check_end and s[i] == ",":
                if type(val) != str:
                    tmp.append(val)
                else:
                    tmp.append(self._deserialize(val))
                val = ""
                i += 1

            if s[i] == "[":
                check_end = False
                open_count += 1
            elif s[i] == "]":
                close_count += 1
            elif s[i] == "{" and check_end:
                val, i = self._deserialize_dict(s, i)
                continue

            if close_count > open_count:
                if type(val) != str:
                    tmp.append(val)
                elif val == "":
                    i+=1
                    return tuple(tmp), i
                else:
                    tmp.append(self._deserialize(val))
                i+=1
                break

            if close_count and close_count == open_count:
                check_end = True
            val += s[i]
            i += 1
        return tuple(tmp), i

    def _deserialize_primitive(self, s: str):
        if s == "null":
            return None
        if s == "true":
            return True
        if s == "false":
            return False
        if re.search(r"\"(.*)\"", s):
            return re.search(r"\"(.*)\"", s).group(1)
        if re.search(r"-?[0-9]+\.[0-9]+", s):
            return float(re.search(r"-?[0-9]+\.[0-9]+", s).group())
        if re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s):
            return complex(re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s).group())
        if re.search(r"-?[0-9]+", s):
            return int(re.search(r"[0-9]+", s).group())

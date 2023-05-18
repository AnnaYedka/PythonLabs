from serializer import Serializer
from consts import PRIMITIVE_TYPES, ITERABLE_TYPES
from Converter import convert, deconvert
import re
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

        tmp = "\n"
        for k, v in obj.items():
            if type(v) in PRIMITIVE_TYPES:
                tmp += "    " * indent + f"<{self._serialize(k, indent + 1)}>{self._serialize(v, indent + 1)}" +\
                        f"</{self._serialize(k, indent + 1)}>" + "\n"
            else:
                tmp += "    "*indent + f"<{self._serialize(k, indent+1)}>{self._serialize(v, indent+1)}" +\
                   "    "*indent + f"</{self._serialize(k, indent+1)}>" + "\n"
        return tmp


    def _deserialize(self, s:str):
        keys = []
        vals = []
        i = 0
        tmp = ""
        has_value = False
        while i < len(s):
            if s[i] == "<":
                if has_value:
                    vals.append(tmp)
                tmp += s[i]
            elif s[i] == ">":
                tmp += s[i]
                keys.append(tmp)
                if tmp == "<list>":
                    vals.append([])
                elif tmp != "<item>":
                    vals.append({})
                tmp = ""
                if i != len(s) and s[i+1] != "<":
                    has_value = True
            elif s[i] == "/":
                tmp = ""
                while s[i] != ">":
                    i += 1
                if keys[-1] == "<item>":
                    vals[-2].append(self._deserialize_obj(vals[-1]))
                    vals.pop()
                    keys.pop()
                else:
                    if len(vals) == 1:
                        if type(vals[0]) == list:
                            return tuple(vals[0])
                        return vals[0]
                    elif type(vals[-1]) == str or type[vals[-1]] == list:
                        vals[-2].update({self._deserialize_obj(keys[-1][1:-1]): self._deserialize_obj(vals[-1])})
                        vals.pop()
                        keys.pop()
                    else:
                        tmp_dict = {}
                        while vals[-1]:
                            tmp_dict.update(vals[-1])
                            vals.pop()
                        vals[-1].update({self._deserialize_obj(keys[-1][1:-1]): tmp_dict})
                        keys.pop()
                has_value = False
            else:
                tmp += s[i]
            i+=1
        res = {}
        for d in vals:
            res.update(d)
        return res

    def _deserialize_obj(self, obj):
        if type(obj) == list:
            return tuple(obj)
        if type(obj) != str:
            return obj
        return self._deserialize_primitive(obj)

    def _deserialize_primitive(self, s: str):
        if s == "None":
            return None
        if s == "True":
            return True
        if s == "False":
            return False
        if re.search(r"-?[0-9]+\.[0-9]+", s):
            return float(re.search(r"-?[0-9]+\.[0-9]+", s).group())
        if re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s):
            return complex(re.search(r"\(-?[0-9]+(\+|-)[0-9]+j\)", s).group())
        if re.search(r"-?[0-9]+", s):
            return int(re.search(r"[0-9]+", s).group())
        return s

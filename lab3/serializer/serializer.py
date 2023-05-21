from .JSONSerializer import JSONSerializer
from .XMLSerializer import XMLSerializer


class Serializer:
    @staticmethod
    def create_serializer(form: str):
        if form == 'json':
            return JSONSerializer()
        elif form == 'xml':
            return XMLSerializer()
        else:
            raise ValueError(f"No type {form}")

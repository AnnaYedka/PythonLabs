import re


class MyContainer:
    def __init__(self):
        self.__container = set()

    def add(self, elements):
        self.__container.update(self.str_to_int(elements))

    def remove(self, key):
        tmp = int(key) if key.isdigit() else key
        self.__container.discard(tmp)

    def find(self, list):
        elements = self.str_to_int(list)
        found = False
        for elem in elements:
            if elem in self.__container:
                found = True
                print(elem)
        if not found:
            print("No such elements")

    def list(self):
        print(", ".join(self.data_to_str()))

    def grep(self, regex):
        found = False
        for elem in self.__container:
            if type(elem) == str:
                found_elements = re.findall(regex, elem)
                if len(found_elements) != 0:
                    print(found_elements)
                    found = True
        if not found:
            print("No such elements")

    def str_to_int(self, elements):
        return [int(elem) if elem.isdigit() else elem for elem in elements]

    def data_to_str(self):
        return [str(item) for item in self.__container]

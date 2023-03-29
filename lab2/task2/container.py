import re

class MyContainer:
    def __init__(self):
        self.__container = set()

    def add(self, elements):
        self.__container.update(elements)

    def remove(self, key):
        self.__container.discard(key)

    def find(self, elements):
        found = False
        for elem in elements:
            if elem in self.__container:
                found = True
                print(elem)
        if not found:
            print("No such elements")

    def list(self):
        print(", ".join(self.__container))

    def grep(self, regex):
        found = False
        for elem in self.__container:
            found_elements = re.findall(regex, elem)
            if len(found_elements) != 0:
                print(found_elements)
                found = True
        if not found:
            print("No such elements")

    def get_data(self):
        return self.__container


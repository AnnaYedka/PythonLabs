import os.path

from container import MyContainer
from constants import FILE_NOT_FOUND



class User:
    def __init__(self, name=None):
        self.__name = name
        self.__container = MyContainer()

    def name(self):
        return self.__name

    def name(self, new_name):
        self.__name = new_name

    def add_data(self, elements):
        self.__container.add(elements)

    def remove_data(self, key):
        self.__container.remove(*key)

    def find_data(self, elements):
        self.__container.find(elements)

    def list_data(self):
        self.__container.list()

    def grep_data(self, regex):
        self.__container.grep(*regex)

    def load_data(self, filename=None):
        if not filename:
            filename = os.path.join("users", self.__name)
        else:
            filename = filename[0]
        try:
            with open(filename, "r") as file:
                self.__container.add(file.read().split(", "))
        except FileNotFoundError:
            print(FILE_NOT_FOUND)

    def save(self):
        filename = os.path.join("users", self.__name)
        with open(filename, "w") as file:
            file.write(", ".join(self.__container.data_to_str()))

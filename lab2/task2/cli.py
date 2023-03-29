from user import User
from constants import (LOAD_ASK, SAVE_ASK, INVALID_CMD, INVALID_ARGS, ESCAPE_CMD)


class System:

    def __init__(self):
        self.__user = User(input("Enter username: "))
        self.__commands = {}

    def update_commands(self):
        self.__commands = {
            "add": self.__user.add_data,
            "remove": self.__user.remove_data,
            "find": self.__user.find_data,
            "list": self.__user.list_data,
            "grep": self.__user.grep_data,
            "save": self.__user.save,
            "load": self.__user.load_data,
            "switch": self.switch
        }

    def switch(self, new_username):
        answ = input(SAVE_ASK)

        if answ == "y":
            self.__user.save()
        self.__user = User(*new_username)
        self.update_commands()

        answ = input(LOAD_ASK)
        if answ == "y":
            self.__user.load_data()

    def parse_command(self, command: str):
        command_with_args = command.split(" ", maxsplit=1)
        if command_with_args[0] not in self.__commands.keys():
            print(INVALID_CMD)
            return "", None
        else:
            return command_with_args[0], command_with_args[1].split(" ") if len(command_with_args) > 1 else None

    def run_command(self, command: str):
        cmd, args = self.parse_command(command)
        if cmd != "":
            if args:
                try:
                    self.__commands[cmd](args)
                except TypeError:
                    print(INVALID_ARGS)
            else:
                try:
                    self.__commands[cmd]()
                except TypeError:
                    print(INVALID_ARGS)

    def run(self):
        self.update_commands()
        while True:
            user_input = input()
            if user_input == ESCAPE_CMD:
                answ = input(SAVE_ASK)
                if answ == "y":
                    self.__user.save()
                break
            self.run_command(user_input)

System().run()
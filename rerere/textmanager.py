# -*- coding: utf-8 -*-
import re


class TextManager:
    def __init__(self, dt):
        self.list = dt.split('\n')
        self.__i = -1
        self.ret = {}

    def move_index_to_same_line(self):
        self.__i -= 1

    def execute(self, command_manager, start=0, end=-1):
        self.__i = start - 1
        try:
            commands = command_manager.next()
            while True:
                self.__i += 1
                if end >= 0 and self.__i >= end:
                    break

                line = self.list[self.__i]

                for mindex, command in enumerate(commands):
                    pattern = re.compile(command.pattern)
                    tmp = pattern.search(line)
                    if tmp:
                        if command.match(tmp):
                            commands = command_manager.next()
                            break
                    else:
                        if command.not_match():
                            commands = command_manager.next()
                            break
            return self.ret
        except IndexError:
            return self.ret

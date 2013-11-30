# -*- coding: utf-8 -*-
import re
import sys
from rerere.command import *

START_SYMBOL = '<<'
END_SYMBOL = '>>'


class CommandManager:

    def __init__(self, mask_str, text_manager):
        self.__i = -1
        self.__commands = []  # 比較中のコマンド
        self.__commands_all = []  # すべてのコマンド
        self.__lines = []  # すべての行（構文解析後)
        self.__loop_counter = {}
        self.command_master = ['@if', '@endif', '@loop', '@endloop', '@any']
        self.text_manager = text_manager

        self.__lines = list(map(lambda x: self.parse(x), mask_str.split('\n')))
        self.__commands_all = list(map(lambda x: self.convert_command(x), self.__lines))

    def parse(self, line):
        if not line:
            line = START_SYMBOL + '@any' + END_SYMBOL  # 空行はanyコマンドにしておく

        command_main = re.compile(r'' + START_SYMBOL + '(.+)' + END_SYMBOL)
        main_str = command_main.search(line)
        ret = {}
        if main_str:
            tmp = re.split(r'\s+', main_str.group(1))
            if tmp[0] in self.command_master:  # コマンドではじまっている
                ret['command_name'] = tmp.pop(0).replace('@', '')
                ret['attributes'] = {x2[0]: x2[1][1:-1] for x2 in [x.split('=') for x in tmp]}
            else:
                # 代入のコマンドとする
                ret['keys'] = [x.replace(START_SYMBOL + '=', '').replace(END_SYMBOL, '') for x in re.findall(r'' + START_SYMBOL + '=' + '[0-9A-z%]+' + END_SYMBOL, line)]
                ret['attributes'] = {}
                ret['attributes']['pattern'] = re.sub(r'' + START_SYMBOL + '=' + '[0-9A-z%]+' + END_SYMBOL, '', line)
                ret['command_name'] = 'search'
        else:
            # ただの正規表現。代入なし
            ret['keys'] = []
            ret['attributes'] = {}
            ret['attributes']['pattern'] = line
            ret['command_name'] = 'search'

        return ret

    def convert_command(self, line):
        class_c = globals()[line['command_name'].capitalize() + 'command']
        obj = class_c(self, self.text_manager, line)
        return obj

    def remove_command(self, obj):
        tmp = [x for x in self.__commands if x == obj]
        if tmp:
            self.__commands.remove(tmp[0])
            return True
        return False

    def set_command(self, obj):
        self.__commands.append(obj)

    def search_command(self, command_name, command_id):
        return self.__search_command(command_name, command_id, self.__commands)

    def search_command_all(self, command_name, command_id):
        return self.__search_command(command_name, command_id, self.__commands_all)

    def __search_command(self, command_name, command_id, obj):
        tmp = [x for x in obj if x.command_name == command_name and x.command_id == command_id]
        if tmp:
            return tmp[0]
        else:
            return None

    def get_command_index(self, obj):
        return self.__get_command_index(obj, self.__commands)

    def get_command_all_index(self, obj):
        return self.__get_command_index(obj, self.__commands_all)

    def __get_command_index(self, target, obj):
        for i, v in enumerate(obj):
            if target == v:
                return i
        return None

    def get_pair_action_name(self, command_name):
        if re.search('end', command_name):
            return command_name.replace('end', '')
        else:
            return 'end' + command_name

    def search_pair_command_index(self, command):
        pair_action_name = self.get_pair_action_name(command.command_name)
        for i, v in enumerate(self.__commands_all):
            if v.command_name == pair_action_name and v.command_id == command.command_id:
                return i
        return None

    def move_index_to_pair_command(self, command):
        self.__i = self.search_pair_command_index(command)

    def add_loop_counter(self, command_id):
        self.__loop_counter[command_id] = self.__loop_counter.get(command_id, 0) + 1

    def clear_loop_counter(self, command_id):
        self.__loop_counter[command_id] = 0

    def create_keys(self, keys):
        counter = {k: v for k, v in self.__loop_counter.items() if v > 0}
        if not counter:
            return keys
        for k, v in counter.items():
            keys = [x.replace('%' + k + '%', str(v)) for x in keys]
        return keys

    def next(self):
        try:
            self.__i += 1
            current_command = self.__commands_all[self.__i]
            if current_command.start():
                return self.next()

            return self.__commands
        except IndexError as e:
            raise e

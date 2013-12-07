# -*- coding: utf-8 -*-
import re
import sys
import uuid
from .command import *

START_SYMBOL = '<<'
END_SYMBOL = '>>'


class CommandManager:

    def __init__(self, mask_str, text_manager):
        self.__i = -1
        self.__commands = []  # 比較中のコマンド
        self.__commands_all = []  # すべてのコマンド
        self.__lines = []  # すべての行（構文解析後)
        self.__loop_counter = {}
        self.__text_manager = text_manager

        self.__lines = list(map(lambda x: self.__parse(x), mask_str.split('\n')))
        self.__commands_all = list(map(lambda x: self.__convert_command(x), self.__lines))
        self.__complement_command_id()
        self.__complement_parent_command_id()

    def __parse(self, line):
        if not line and START_SYMBOL + "#" in line:  # まずコメントをきれいに無くす
            line = line[0: line.find(START_SYMBOL + "#")]

        if not line:
            line = START_SYMBOL + '@any' + END_SYMBOL  # 空行はanyコマンドにしておく

        command_main = re.compile(r'' + START_SYMBOL + '(.+)' + END_SYMBOL)
        main_str = command_main.search(line)
        ret = {}
        if main_str:
            tmp = re.split(r'\s+', main_str.group(1))
            if '@' in tmp[0]:
                ret['command_name'] = tmp.pop(0).replace('@', '')
                ret['attributes'] = {x2[0].strip(' \'"'): x2[1].strip(' \'"') for x2 in [x.split('=') for x in tmp]}
            else:
                # 代入のコマンドとする
                ret['keys'] = [x.replace(START_SYMBOL + '=', '').replace(END_SYMBOL, '') for x in re.findall(r'' + START_SYMBOL + '=' + '[0-9A-z%\[\]\+]+' + END_SYMBOL, line)]
                ret['attributes'] = {}
                ret['attributes']['pattern'] = re.sub(r'' + START_SYMBOL + '=' + '[0-9A-z%\[\]\+]+' + END_SYMBOL, '', line)
                ret['command_name'] = 'search'
        else:
            # ただの正規表現。代入なし
            ret['keys'] = []
            ret['attributes'] = {}
            ret['attributes']['pattern'] = line
            ret['command_name'] = 'search'

        return ret

    def __convert_command(self, line):
        class_c = globals()[line['command_name'].capitalize() + 'command']
        obj = class_c(self, self.__text_manager, line)
        return obj

    def __complement_command_id(self):
        block = {}

        def set_block(command_name, command_id):
            if not command_name in block:
                block[command_name] = []
            block[command_name].append(command_id)

        def get_current_command_id(command_name):
            return block.get(command_name, [])[-1]

        def delete_current_command_id(command_name):
            block.get(command_name, []).pop()

        for i, command in enumerate(self.__commands_all):
            if not command.is_block_command:
                continue
            if command.is_block_start:
                if not command.command_id:
                    command.command_id = str(uuid.uuid4())
                set_block(command.command_name, command.command_id)
            else:
                command.command_id = get_current_command_id(command.pair_command_name)
                delete_current_command_id(command.pair_command_name)

    def __complement_parent_command_id(self):
        block = {}

        def set_block(command_name, command_id):
            if not command_name in block:
                block[command_name] = []
            block[command_name].append(command_id)

        def get_all_command_ids():
            ret = []
            for k, v in block.items():
                ret += v
            return ret

        def delete_current_command_id(command_name):
            block.get(command_name, []).pop()

        for i, command in enumerate(self.__commands_all):
            command.parent_block_command_ids = get_all_command_ids()
            if command.is_block_command:
                if command.is_block_start:
                    set_block(command.command_name, command.command_id)
                else:
                    delete_current_command_id(command.pair_command_name)

    def remove_command(self, obj):
        tmp = [x for x in self.__commands if x == obj]
        if tmp:
            self.__commands.remove(tmp[0])
            return True
        return False

    def remove_child_commands(self, obj):
        if not obj.command_id:
            return False
        for x in self.__commands:
            if obj.command_id in x.parent_block_command_ids:
                self.remove_command(x)
        return True

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

    def get_commands_all(self):
        return self.__commands_all

    def get_commands(self):
        return self.__commands

    def search_pair_command_index(self, command):
        for i, v in enumerate(self.__commands_all):
            if v.command_name == command.pair_command_name and v.command_id == command.command_id:
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

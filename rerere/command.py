# -*- coding: utf-8 -*-


class Command:

    command_name = None

    def __init__(self, command_manager, text_manager, line):
        self.command_manager = command_manager
        self.text_manager = text_manager
        self.keys = line.get('keys', [])
        self.pattern = line.get('attributes', {}).get('pattern', '')
        self.command_id = line.get('attributes', {}).get('id', '')

    def __str__(self):
        ret = self.command_name
        ret += ' / keys:' + ','.join(self.keys)
        ret += ' / pattern:' + self.pattern
        ret += ' / command_id:' + self.command_id
        return ret

    def __repr__(self):
        ret = self.command_name
        ret += ' / keys:' + ','.join(self.keys)
        ret += ' / pattern:' + self.pattern
        ret += ' / command_id:' + self.command_id
        return ret


class Anycommand(Command):

    command_name = 'any'

    def start(self):
        return True

    def match(self, search):
        return True

    def not_match(self):
        return False


class Ifcommand(Command):

    command_name = 'if'

    def start(self):
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        return True

    def not_match(self):
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.text_manager.move_index_to_same_line()
        return True


class Endifcommand(Command):

    command_name = 'endif'

    def start(self):
        return True

    def match(self, search):
        return True

    def not_match(self):
        return False


class Loopcommand(Command):

    command_name = 'loop'

    def start(self):
        self.command_manager.add_loop_counter(self.command_id)
        self.command_manager.set_command(self)
        return True

    def match(self, search):
        self.command_manager.clear_loop_counter(self.command_id)
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        return True

    def not_match(self):
        return False


class Endloopcommand(Command):

    command_name = 'endloop'

    def start(self):
        # loopの終了合図が見つからないままendに来てしまった。loopの先頭へ戻る
        self.command_manager.add_loop_counter(self.command_id)
        self.command_manager.move_index_to_pair_command(self)
        return True

    def match(self, search):
        return True

    def not_match(self):
        return False


class Searchcommand(Command):

    command_name = 'search'

    def start(self):
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        if self.keys:
            for i, key in enumerate(self.command_manager.create_keys(self.keys)):
                self.text_manager.ret[key] = search.group(i + 1)
        self.command_manager.remove_command(self)
        return True

    def not_match(self):
        return False

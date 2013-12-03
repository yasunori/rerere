# -*- coding: utf-8 -*-


class Command:
    """
    コマンドを表します
    """

    command_name = None
    pair_command_name = None
    is_block_command = False
    is_block_start = False
    parent_block_command_ids = []

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
        ret += ' / parent_block_command_ids:' + ','.join(self.parent_block_command_ids)
        return ret

    def __repr__(self):
        ret = self.command_name
        ret += ' / keys:' + ','.join(self.keys)
        ret += ' / pattern:' + self.pattern
        ret += ' / command_id:' + self.command_id
        ret += ' / parent_block_command_ids:' + ','.join(self.parent_block_command_ids)
        ret += '\n'
        return ret

    def start(self):
        """
        コマンドマネージャがこのコマンドにカーソルを合わせたときに呼ばれる関数。
        正規表現としての評価はまだ実施されていません。
        @return 評価するコマンドリストのカーソルを次行へ進めて再帰的にコマンド構築処理をする場合True
        """
        return False

    def match(self, search):
        """
        マッチしたときに呼ばれる関数。
        @param search マッチしたオブジェクト
        @return 評価対象のテキストのカーソルを次行へ進める場合True
        """
        return True

    def not_match(self):
        """
        マッチしなかったときに呼ばれる関数。
        @return 評価対象のテキストのカーソルを次行へ進める場合True
        """
        return False


class Anycommand(Command):

    command_name = 'any'
    pair_command_name = None
    is_block_command = False
    is_block_start = False

    def start(self):
        return True

    def match(self, search):
        return True

    def not_match(self):
        return False


class Ifcommand(Command):

    command_name = 'if'
    pair_command_name = 'endif'
    is_block_command = True
    is_block_start = True

    def start(self):
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        self.command_manager.remove_command(self)
        self.text_manager.move_index_to_same_line()
        return True

    def not_match(self):
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.text_manager.move_index_to_same_line()
        return True


class Endifcommand(Command):

    command_name = 'endif'
    pair_command_name = 'if'
    is_block_command = True
    is_block_start = False

    def start(self):
        return True

    def match(self, search):
        return True

    def not_match(self):
        return False


class Loopcommand(Command):

    command_name = 'loop'
    pair_command_name = 'endloop'
    is_block_command = True
    is_block_start = True

    def start(self):
        self.command_manager.add_loop_counter(self.command_id)
        self.command_manager.set_command(self)
        return True

    def match(self, search):
        self.command_manager.clear_loop_counter(self.command_id)
        self.command_manager.move_index_to_pair_command(self)
        self.command_manager.remove_command(self)
        self.command_manager.remove_child_commands(self)
        return True

    def not_match(self):
        return False


class Endloopcommand(Command):

    command_name = 'endloop'
    pair_command_name = 'loop'
    is_block_command = True
    is_block_start = False

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
    pair_command_name = None
    is_block_command = False

    def start(self):
        self.command_manager.set_command(self)
        return False

    def match(self, search):
        if self.keys:
            for i, key in enumerate(self.command_manager.create_keys(self.keys)):
                if '[]' in key:
                    key = key.replace('[]', '')
                    if not key in self.text_manager.ret:
                        self.text_manager.ret[key] = []
                    self.text_manager.ret[key].append(search.group(i + 1))
                else:
                    self.text_manager.ret[key] = search.group(i + 1)
        self.command_manager.remove_command(self)
        return True

    def not_match(self):
        return False

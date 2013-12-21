# -*- coding: utf-8 -*-
from nose.tools import ok_, eq_, with_setup, raises
import rerere
from rerere.command import CommandException


@raises(CommandException)
def ng_command_1_test():
    '''
    そんなコマンドが無いパターン
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@anya>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_none_1_test():
    '''
    コマンドに属性が1個もないパターン(必須なものが無いほうに)
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_none_2_test():
    '''
    コマンドに属性が1個もないパターン(スペースがあるのでパースで落ちる)
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if >>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_error_1_test():
    '''
    コマンドの属性がおかしいパターン
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if a>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_error_2_test():
    '''
    コマンドの属性がおかしいパターンその2
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if a=>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_error_3_test():
    '''
    コマンドの属性がおかしいパターンその3
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if a="a>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


def ng_command_attribute_error_4_test():
    '''
    コマンドの属性がおかしいパターンその4。
    これは救う。
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if match = "an">>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


def ng_command_attribute_error_5_test():
    '''
    コマンドの属性がおかしいパターンその5。
    これは救う。
    '''

    txt = '''
あいうえお
an
かきくけこ
'''
    re_txt = '''
<<@if match =   "an">>
(\S+)<<=test>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    ok_(ret['test'], 'an')


def ng_command_attribute_error_6_test():
    '''
    コマンドの最後がおかしいパターンその6。
    これは救う。
    '''

    txt = '''
あいうえお
an
かきくけこ
'''
    re_txt = '''
<<@if match="an" >>
(\S+)<<=test>>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    ok_(ret['test'], 'an')



@raises(CommandException)
def ng_command_attribute_if_test():
    '''
    必須属性が無いパターン if
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if matchee="(\S+)">>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_block_test():
    '''
    必須属性が無いパターン block
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@block machee="(\S+)">>
<<@endblock>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_attribute_loop_test():
    '''
    必須属性が無いパターン loop
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@loop matchee="(\S+)">>
<<@endloop>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_if_test():
    '''
    ペアが無いパターン if
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if match="(\S+)">>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_blick_test():
    '''
    ペアが無いパターン block
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@block match="(\S+)">>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_loop_test():
    '''
    ペアが無いパターン loop
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@loop match="(\S+)">>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_if_2_test():
    '''
    ペアが無いパターン 2階層 if
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@if match="(\S+)">>
  <<@if match="(\S+)">>
<<@endif>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_block_2_test():
    '''
    ペアが無いパターン 2階層 block
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@block match="(\S+)">>
  <<@block match="(\S+)">>
<<@endblock>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)


@raises(CommandException)
def ng_command_pair_loop_2_test():
    '''
    ペアが無いパターン 2階層 loop
    '''

    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@loop match="(\S+)">>
  <<@loop match="(\S+)">>
<<@endloop>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    text_manager.execute(command_manager=command_manager)

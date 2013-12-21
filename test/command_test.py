# -*- coding: utf-8 -*-
import sys
from nose.tools import ok_, eq_, with_setup
import rerere


def setup():
    pass


def teardown():
    pass


def any_test():
    txt = '''
あいうえお
かきくけこ
'''
    re_txt = '''
<<@any>>
<<@any>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret, {})


def search_1_test():
    txt = '''
[商品]あいうえお(新発売)
[個数]3個
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>>
\[個数\]([0-9])<<=item_count>>個
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['item_count'], '3')


def search_2_test():
    '''
    1行に複数のグループがある場合
    '''

    txt = '''
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>> ※(\S+)<<=additional_info>>
\[個数\]([0-9])<<=item_count>>個
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['additional_info'], '12/1新発売')
    eq_(ret['item_count'], '3')


def search_3_test():
    '''
    リストに代入する場合
    '''

    txt = '''
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
[紹介]
これはとても良い商品です。
新鮮でおいしいよ。
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>> ※(\S+)<<=additional_info>>
\[個数\]([0-9])<<=item_count>>個
\[紹介\]
(.+)<<=item_detail[]>>
(.+)<<=item_detail[]>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['additional_info'], '12/1新発売')
    eq_(ret['item_count'], '3')
    eq_(ret['item_detail'][0], 'これはとても良い商品です。')
    eq_(ret['item_detail'][1], '新鮮でおいしいよ。')


def search_4_test():
    '''
    結合する場合
    '''

    txt = '''
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
[紹介]
これはとても良い商品です。
新鮮でおいしいよ。
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>> ※(\S+)<<=additional_info>>
\[個数\]([0-9])<<=item_count>>個
\[紹介\]
(.+)<<=item_detail+>>
(.+)<<=item_detail+>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['additional_info'], '12/1新発売')
    eq_(ret['item_count'], '3')
    eq_(ret['item_detail'], 'これはとても良い商品です。新鮮でおいしいよ。')


def search_5_test():
    '''
    すぐ判断する場合 OKの場合
    '''

    txt = '''
[商品]あいうえお(新発売)
[個数]3個
[備考]あああ
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>>
\[個数\]([0-9])<<=item_count !>>個
\[備考\](\S+)<<=item_comment>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['item_count'], '3')
    eq_(ret['item_comment'], 'あああ')


def search_6_test():
    '''
    すぐ判断する場合 NGの場合 空行のせいで駄目
    '''

    txt = '''
[商品]あいうえお(新発売)

[個数]3個
[備考]あああ
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>>
\[個数\]([0-9])<<=item_count !>>個
\[備考\](\S+)<<=item_comment>>
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret.get('item_count', None), None)
    eq_(ret['item_comment'], 'あああ')


def search_7_test():
    '''
    判断あとでもいい場合
    '''

    txt = '''
[商品]あいうえお(新発売)
[個数]3個
[備考]あああ
'''
    re_txt = '''
\[商品\](\S+)<<=item_name>>
\[備考\](\S+)<<=item_comment ?>>
\[個数\]([0-9])<<=item_count>>個
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'], 'あいうえお(新発売)')
    eq_(ret['item_count'], '3')
    eq_(ret['item_comment'], 'あああ')


def if_1_test():
    '''
    if okのパターン
    '''

    txt = '''
購入リスト
--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
--------
[商品]かきくけこ ※12/2新発売
[個数]1個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['additional_info'][1], '12/2新発売')
    eq_(ret['item_count'][1], '1')
    eq_(ret['total'], '1000')


def if_2_test():
    '''
    if 1つないパターン
    '''

    txt = '''
購入リスト
--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['total'], '1000')



def if_3_test():
    '''
    if 入れ子パターン ある
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個
--------
パッケージ2
　******
　[商品]さしすせそ
　[個数]4個
　******
　[商品]たちつてと
　[個数]5個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endif>>
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお')
    eq_(ret['item_count'][0], '2')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['item_count'][1], '3')
    eq_(ret['item_name'][2], 'さしすせそ')
    eq_(ret['item_count'][2], '4')
    eq_(ret['item_name'][3], 'たちつてと')
    eq_(ret['item_count'][3], '5')
    eq_(ret['total'], '1000')


def if_4_test():
    '''
    if 入れ子パターン なし1
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endif>>
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお')
    eq_(ret['item_count'][0], '2')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['item_count'][1], '3')
    eq_(ret['total'], '1000')


def if_5_test():
    '''
    if 入れ子パターン なし2
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
--------
パッケージ2
　******
　[商品]さしすせそ
　[個数]4個
　******
　[商品]たちつてと
　[個数]5個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*" exit="\-\-\-">>
\*\*\*
\[商品\](\S+)<<=item_name_p1[]>>
\[個数\]([0-9])<<=item_count_p1[]>>個
<<@endif>>
<<@if match="\*\*\*\*" exit="\-\-\-">>
\*\*\*
\[商品\](\S+)<<=item_name_p1[]>>
\[個数\]([0-9])<<=item_count_p1[]>>個
<<@endif>>
<<@endif>>
<<@if match="\-\-\-\-\-">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name_p2[]>>
\[個数\]([0-9])<<=item_count_p2[]>>個
<<@endif>>
<<@if match="\*\*\*\*">>
\*\*\*
\[商品\](\S+)<<=item_name_p2[]>>
\[個数\]([0-9])<<=item_count_p2[]>>個
<<@endif>>
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''
    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name_p1'][0], 'あいうえお')
    eq_(ret['item_count_p1'][0], '2')
    eq_(ret['item_name_p2'][0], 'さしすせそ')
    eq_(ret['item_count_p2'][0], '4')
    eq_(ret['item_name_p2'][1], 'たちつてと')
    eq_(ret['item_count_p2'][1], '5')
    eq_(ret['total'], '1000')


def if_6_test():
    '''
    if 入れ子パターン なし2 limitつかう
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
--------
パッケージ2
　******
　[商品]さしすせそ
　[個数]4個
　******
　[商品]たちつてと
　[個数]5個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-\-" limit="1">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*" limit="1">>
\*\*\*
\[商品\](\S+)<<=item_name_p1[]>>
\[個数\]([0-9])<<=item_count_p1[]>>個
<<@endif>>
<<@if match="\*\*\*\*" limit="1">>
\*\*\*
\[商品\](\S+)<<=item_name_p1[]>>
\[個数\]([0-9])<<=item_count_p1[]>>個
<<@endif>>
<<@endif>>
<<@if match="\-\-\-\-\-" limit="1">>
\-\-\-\-\-
パッケージ
<<@if match="\*\*\*\*" limit="1">>
\*\*\*
\[商品\](\S+)<<=item_name_p2[]>>
\[個数\]([0-9])<<=item_count_p2[]>>個
<<@endif>>
<<@if match="\*\*\*\*" limit="1">>
\*\*\*
\[商品\](\S+)<<=item_name_p2[]>>
\[個数\]([0-9])<<=item_count_p2[]>>個
<<@endif>>
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''
    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name_p1'][0], 'あいうえお')
    eq_(ret['item_count_p1'][0], '2')
    eq_(ret['item_name_p2'][0], 'さしすせそ')
    eq_(ret['item_count_p2'][0], '4')
    eq_(ret['item_name_p2'][1], 'たちつてと')
    eq_(ret['item_count_p2'][1], '5')
    eq_(ret['total'], '1000')



def loop_1_test():
    '''
    loop okのパターン
    '''

    txt = '''
購入リスト
--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
--------
[商品]かきくけこ ※12/2新発売
[個数]1個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['additional_info'][1], '12/2新発売')
    eq_(ret['item_count'][1], '1')
    eq_(ret['total'], '1000')


def loop_2_test():
    '''
    loop okのパターン
    '''

    txt = '''
購入リスト


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['total'], '1000')


def loop_3_test():
    '''
    loop 入れ子パターン ある
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個
--------
パッケージ2
　******
　[商品]さしすせそ
　[個数]4個
　******
　[商品]たちつてと
　[個数]5個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額">>
\-\-\-\-\-
パッケージ
<<@loop exit="\-\-\-\-">>
\*\*\*
\[商品\](\S+)<<=item_name[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endloop>>
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお')
    eq_(ret['item_count'][0], '2')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['item_count'][1], '3')
    eq_(ret['item_name'][2], 'さしすせそ')
    eq_(ret['item_count'][2], '4')
    eq_(ret['item_name'][3], 'たちつてと')
    eq_(ret['item_count'][3], '5')
    eq_(ret['total'], '1000')


def loop_4_test():
    '''
    loop 入れ子パターン ある with id
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個
--------
パッケージ2
　******
　[商品]さしすせそ
　[個数]4個
　******
　[商品]たちつてと
　[個数]5個

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額" id="loop1">>
\-\-\-\-\-
パッケージ
<<@loop exit="\-\-\-\-" id="loop2">>
\*\*\*
\[商品\](\S+)<<=item_name_%loop1%[]>>
\[個数\]([0-9])<<=item_count_%loop1%[]>>個
<<@endloop>>
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name_1'][0], 'あいうえお')
    eq_(ret['item_count_1'][0], '2')
    eq_(ret['item_name_1'][1], 'かきくけこ')
    eq_(ret['item_count_1'][1], '3')
    eq_(ret['item_name_2'][0], 'さしすせそ')
    eq_(ret['item_count_2'][0], '4')
    eq_(ret['item_name_2'][1], 'たちつてと')
    eq_(ret['item_count_2'][1], '5')
    eq_(ret['total'], '1000')


def loop_5_test():
    '''
    loop 入れ子パターン ない1
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個
--------
パッケージ2

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額" id="loop1">>
\-\-\-\-\-
パッケージ
<<@loop exit="\-\-\-\-" id="loop2">>
\*\*\*
\[商品\](\S+)<<=item_name_%loop1%[]>>
\[個数\]([0-9])<<=item_count_%loop1%[]>>個
<<@endloop>>
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name_1'][0], 'あいうえお')
    eq_(ret['item_count_1'][0], '2')
    eq_(ret['item_name_1'][1], 'かきくけこ')
    eq_(ret['item_count_1'][1], '3')
    eq_(ret['total'], '1000')


def ifd_1_test():
    '''
    ifd okのパターン
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
--------
[商品]かきくけこ ※12/2新発売
[個数]1個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['item_name'][1], 'かきくけこ')
    eq_(ret['additional_info'][1], '12/2新発売')
    eq_(ret['item_count'][1], '1')
    eq_(ret['total'], '1000')


def if_2_test():
    '''
    if 探しに行ってtxtの最後まで行ってしまうが、戻れるパターン
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['total'], '1000')


def ifd_3_test():
    '''
    ifd exitを指定したから抜けられるパターン
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['total'], '1000')


def ifd_4_test():
    '''
    ifd exitを指定したとき、ちゃんとtxtの評価がなかったことになってるテスト
    備考が取得できるかどうか
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個

[備考]びこうだよ

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

\[備考\](\S+)<<=comment>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['comment'], 'びこうだよ')
    eq_(ret['total'], '1000')


def ifd_5_test():
    '''
    ifd exitを指定しても、一旦idfの中にはいってしまったら効かない
    探しにいったまま終わる
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売


[備考]びこうだよ

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

\[備考\](\S+)<<=comment>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret.get('comment', None), None)
    eq_(ret.get('total', None), None)


def ifd_6_test():
    '''
    まあこうすれば取れる。
    あるか分からなかったらifdで囲んでおく
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売


[備考]びこうだよ

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
<<@if match="個数" exit="合計金額">>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endif>>

<<@if match="\-\-\-\-" exit="合計金額">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

\[備考\](\S+)<<=comment>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['comment'], 'びこうだよ')
    eq_(ret['total'], '1000')


def ifd_7_test():
    '''
    ifd ここでちょっとlimitのテスト
    '''

    txt = '''
購入リスト
--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個
--------
[商品]かきくけこ(新発売) ※12/3新発売
[個数]4個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" limit="1">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" limit="1">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['item_name'][1], 'かきくけこ(新発売)')
    eq_(ret['additional_info'][1], '12/3新発売')
    eq_(ret['item_count'][1], '4')
    eq_(ret['total'], '1000')


def ifd_8_test():
    '''
    ifd ここでちょっとlimitのテスト2
    '''

    txt = '''
購入リスト

--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個

--------
[商品]かきくけこ(新発売) ※12/3新発売
[個数]4個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" limit="1">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" limit="1">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret.get('item_name', None), None)
    eq_(ret['total'], '1000')


def ifd_9_test():
    '''
    ifd ここでちょっとlimitのテスト3
    '''

    txt = '''
購入リスト

--------
[商品]あいうえお(新発売) ※12/1新発売
[個数]3個

--------
[商品]かきくけこ(新発売) ※12/3新発売
[個数]4個


合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@if match="\-\-\-\-" limit="2">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-" limit="2">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>


合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['item_count'][0], '3')
    eq_(ret['item_name'][1], 'かきくけこ(新発売)')
    eq_(ret['additional_info'][1], '12/3新発売')
    eq_(ret['item_count'][1], '4')
    eq_(ret['total'], '1000')


def block_1_test():
    '''
    blockで解決
    '''

    txt = '''
購入リスト


--------
[商品]あいうえお(新発売) ※12/1新発売


[備考]びこうだよ

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@block exit="備考">>
<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>

<<@if match="\-\-\-\-">>
\-\-\-\-\-
\[商品\](\S+)<<=item_name[]>> ※(\S+)<<=additional_info[]>>
\[個数\]([0-9])<<=item_count[]>>個
<<@endif>>
<<@endblock>>
\[備考\](\S+)<<=comment>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    ret = text_manager.execute(command_manager=command_manager)
    eq_(ret['item_name'][0], 'あいうえお(新発売)')
    eq_(ret['additional_info'][0], '12/1新発売')
    eq_(ret['comment'], 'びこうだよ')
    eq_(ret['total'], '1000')


def str_test():
    '''
    コマンドのstr化
    '''

    txt = '''
購入リスト
--------
パッケージ1
　******
　[商品]あいうえお
　[個数]2個
　******
　[商品]かきくけこ
　[個数]3個
--------
パッケージ2

合計金額: 1000円
'''
    re_txt = '''
購入リスト
<<@loop exit="合計金額" id="loop1">>
\-\-\-\-\-
パッケージ
<<@loop exit="\-\-\-\-" id="loop2">>
\*\*\*
\[商品\](\S+)<<=item_name_%loop1%[]>>
\[個数\]([0-9])<<=item_count_%loop1%[]>>個
<<@endloop>>
<<@endloop>>

合計金額: ([0-9]+)<<=total>>円
'''

    text_manager = rerere.TextManager(txt)
    command_manager = rerere.CommandManager(re_txt, text_manager)
    commands = str(command_manager.get_commands_all())




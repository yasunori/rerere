# -*- coding: utf-8 -*-
from nose.tools import ok_, eq_, with_setup
import rerere


test1 = '''
このメールは受注メールです。
---------------------------------------------------------------------
[受注番号] 200068-20130000-0538897137
[日時]     2013-08-15 18:18:46
[注文者]   あいうえお (アイウエオ) 様
           〒111-2222 東京都渋谷区1-1-1
           (TEL) 111-2222-3333

[支払方法] クレジットカード決済 一括払い
[ポイント利用方法] なし
[配送方法] 宅配便
[備考]
備考欄

[ショップ名]   さわやかショップ
==========
[送付先]   そうふさき (ソウフサキ) 様
           〒999-8888 北海道札幌市1-1-1
           (TEL) 777-555-4444
[商品]
かっこいい商品1
価格  599(円) x 1(個) = 599(円)   (税込、送料込)
獲得ポイント5
----------
かっこいい商品2
価格  1,180(円) x 1(個) = 1,180(円)   (税込、送料込)
獲得ポイント11
----------
かっこいい商品3
価格  12,444(円) x 1(個) = 12,444(円)   (税込、送料込)
獲得ポイント11

*********************************************************************
小計     1,779(円)
消費税   0(円)
送料     0(円)
---------------------------------------------------
合計     1,779(円)
---------------------------------------------------------------------
今回のお買い物で獲得するポイント　16
---------------------------------------------------------------------
その他
'''

test2 = '''
このメールは受注メールです。
---------------------------------------------------------------------
[受注番号] 200068-20130000-0538897137
[日時]     2013-08-15 18:18:46
[注文者]   あいうえお (アイウエオ) 様
           〒111-2222 東京都渋谷区1-1-1
           (TEL) 111-2222-3333

[支払方法] クレジットカード決済 一括払い
[ポイント利用方法] なし
[配送方法] 宅配便
[備考]
備考欄

[ショップ名]   さわやかショップ
==========
[送付先]   そうふさき (ソウフサキ) 様
           〒999-8888 北海道札幌市1-1-1
           (TEL) 777-555-4444
[商品]
かっこいい商品1
価格  599(円) x 1(個) = 599(円)   (税込、送料込)
獲得ポイント5

*********************************************************************
小計     1,779(円)
消費税   0(円)
送料     0(円)
---------------------------------------------------
合計     1,779(円)
---------------------------------------------------------------------
今回のお買い物で獲得するポイント　16
---------------------------------------------------------------------
その他
'''


mask1 = '''
\[受注番号\]\s*([0-9-]+)<<=order_no>>
\[日時\]\s*([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})<<=insert_date>>
\[注文者\]\s*(\S+)<<=name>> \((\S+)<<=name_kana>>\) 様
\s*〒([0-9]{3}\-[0-9]{4})<<=zip>>\s*(\S+$)<<=address>>
\s*\(TEL\)\s([0-9-]+)<<=phone_number>>

\[商品\]
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント

<<@if match="\-\-\-\-" exit="\*\*\*\*">>
\-\-\-\-\-
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
<<@endif>>

<<@if match="\-\-\-\-" exit="\*\*\*\*">>
\-\-\-\-\-
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
<<@endif>>

<<@if match="\-\-\-\-" exit="\*\*\*\*">>
\-\-\-\-\-
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
<<@endif>>

<<@if match="\-\-\-\-" exit="\*\*\*\*">>
\-\-\-\-\-
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
<<@endif>>

小計\s*([0-9,]+)<<=total_sub>>\(円\)
消費税\s*([0-9]+)<<=tax>>\(円\)
送料\s*([0-9,]+)<<=postage>>\(円\)
\-\-\-\-\-\-
合計\s*([0-9,]+)<<=total>>\(円\)
'''


mask2 = '''
\[受注番号\]\s*([0-9-]+)<<=order_no>>
\[日時\]\s*([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})<<=insert_date>>
\[注文者\]\s*(\S+)<<=name>> \((\S+)<<=name_kana>>\) 様
\s*〒([0-9]{3}\-[0-9]{4})<<=zip>>\s*(\S+$)<<=address>>
\s*\(TEL\)\s([0-9-]+)<<=phone_number>>

\[商品\]
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント

<<@loop exit='\*\*\*\*\*'>>
\-\-\-\-\-
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
<<@endloop>>

小計\s*([0-9,]+)<<=total_sub>>\(円\)
消費税\s*([0-9]+)<<=tax>>\(円\)
送料\s*([0-9,]+)<<=postage>>\(円\)
\-\-\-\-\-\-
合計\s*([0-9,]+)<<=total>>\(円\)
'''

mask3 = '''
\[受注番号\]\s*([0-9-]+)<<=order_no>>
\[日時\]\s*([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})<<=insert_date>>
\[注文者\]\s*(\S+)<<=name>> \((\S+)<<=name_kana>>\) 様
\s*〒([0-9]{3}\-[0-9]{4})<<=zip>>\s*(\S+$)<<=address>>
\s*\(TEL\)\s([0-9-]+)<<=phone_number>>

\[商品\]
<<@loop exit='\*\*\*\*\*'>>
(^.+$)<<=item_name[]>>
価格\s*([0-9,]+)<<=item_price[]>>\(円\) x ([0-9,]+)<<=item_number[]>>\(個\) = ([0-9,]+)<<=item_total[]>>\(円\)
獲得ポイント
\-\-\-\-\-
<<@endloop>>

小計\s*([0-9,]+)<<=total_sub>>\(円\)
消費税\s*([0-9]+)<<=tax>>\(円\)
送料\s*([0-9,]+)<<=postage>>\(円\)
\-\-\-\-\-\-
合計\s*([0-9,]+)<<=total>>\(円\)
'''


def setup():
    pass


def teardown():
    pass


def it_1_test():
    ret = rerere.search(mask1, test1)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['item_name'][1], 'かっこいい商品2')
    eq_(ret['item_price'][1], '1,180')
    eq_(ret['item_number'][1], '1')
    eq_(ret['item_total'][1], '1,180')
    eq_(ret['item_name'][2], 'かっこいい商品3')
    eq_(ret['item_price'][2], '12,444')
    eq_(ret['item_number'][2], '1')
    eq_(ret['item_total'][2], '12,444')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


def it_2_test():
    ret = rerere.search(mask2, test1)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['item_name'][1], 'かっこいい商品2')
    eq_(ret['item_price'][1], '1,180')
    eq_(ret['item_number'][1], '1')
    eq_(ret['item_total'][1], '1,180')
    eq_(ret['item_name'][2], 'かっこいい商品3')
    eq_(ret['item_price'][2], '12,444')
    eq_(ret['item_number'][2], '1')
    eq_(ret['item_total'][2], '12,444')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


def it_3_test():
    ret = rerere.search(mask3, test1)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['item_name'][1], 'かっこいい商品2')
    eq_(ret['item_price'][1], '1,180')
    eq_(ret['item_number'][1], '1')
    eq_(ret['item_total'][1], '1,180')
    eq_(ret['item_name'][2], 'かっこいい商品3')
    eq_(ret['item_price'][2], '12,444')
    eq_(ret['item_number'][2], '1')
    eq_(ret['item_total'][2], '12,444')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


def it_4_test():
    ret = rerere.search(mask1, test2)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


def it_5_test():
    ret = rerere.search(mask2, test2)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


def it_6_test():
    ret = rerere.search(mask3, test2)
    eq_(ret['order_no'], '200068-20130000-0538897137')
    eq_(ret['insert_date'], '2013-08-15 18:18:46')
    eq_(ret['name'], 'あいうえお')
    eq_(ret['name_kana'], 'アイウエオ')
    eq_(ret['zip'], '111-2222')
    eq_(ret['address'], '東京都渋谷区1-1-1')
    eq_(ret['phone_number'], '111-2222-3333')
    eq_(ret['item_name'][0], 'かっこいい商品1')
    eq_(ret['item_price'][0], '599')
    eq_(ret['item_number'][0], '1')
    eq_(ret['item_total'][0], '599')
    eq_(ret['total_sub'], '1,779')
    eq_(ret['tax'], '0')
    eq_(ret['postage'], '0')
    eq_(ret['total'], '1,779')


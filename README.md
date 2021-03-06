rerere
======

### これは何？
rerereは、複数行の被検索文字列に対して、複数行の正規表現を適用します。グループ化した正規表現にマッチした箇所を変数に代入して結果として返します。

被検索文字列のフォーマット情報とロジック本体を分離することが目的です。

### 何が嬉しいの？
- 被検索文字列を解析するためのコード、を書かなくて良くなります。代わりに構造を正規表現と簡単な命令で表現します。
- 構造は、被検索文字列をもとに、取得したい場所を正規表現で書き換えていく感じで簡単に作れます。
- 被検索文字列のフォーマットに変更があったときは、構造の部分に手を入れるだけです。


### 具体例
楽天の自動受注メールを解析してみます。

```
rakuten_mail_plain_txt =
'''
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
'''
```


上の文字列を正規表現で置き換えます。
要らない行はどんどん飛ばして問題ありませんが、要所要所は残したほうが良いかもしれません。
取得したい部分はグループにして、後ろに<<=key>>の形で代入の命令を書きます。
@loop @if @block の制御命令が使えます。(あとで書く)

```
pattern = 
'''
\[受注番号\]\s*([0-9-]+)<<=order_no>>
\[日時\]\s*([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})<<=insert_date>>
\[注文者\]\s*(\S+)<<=name>> \((\S+)<<=name_kana>>\) 様
\s*〒([0-9]{3}\-[0-9]{4})<<=zip>>\s*(\S+$)<<=address>>
\s*\(TEL\)\s([0-9-]+)<<=phone_number>>

\[商品\]
<<@loop exit='\*\*\*\*\*'>> <<# ****が来るまで、このブロック内の順番で検索と取得繰り返し これはコメント>>
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
```


実行
```
ret = rerere.search(pattern, rakuten_mail_plain_txt)
print(ret)
{'item_name': ['かっこいい商品1', 'かっこいい商品2', 'かっこいい商品3'], 'address': '東京都渋谷区1-1-1', 'name_kana': 'アイウエオ', 'item_number': ['1', '1', '1'], 'total_sub': '1,779', 'item_total': ['599', '1,180', '12,444'], 'insert_date': '2013-08-15 18:18:46', 'postage': '0', 'zip': '111-2222', 'tax': '0', 'item_price': ['599', '1,180', '12,444'], 'total': '1,779', 'name': 'あいうえお', 'order_no': '200068-20130000-0538897137', 'phone_number': '111-2222-3333'}
```

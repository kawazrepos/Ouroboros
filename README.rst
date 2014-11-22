Ouroboros
==============

Ouroboros is the database converter from Kawaz2 to Kawaz3.

必要環境
===================

- Python3.3++

セットアップ
====================

::

  $ pip install -r requirements.txt
  $ python converter.py


変換方法
====================

現段階ではMySQLの変換のみをサポート。SQLiteはちゃんと動くか未確認

MySQL（推奨）
----------------------

1. Kawaz3rdをsyncdbする
~~~~~~~~~~~~~~~~~~~

`local_settings.py`のENGINEをMySQLに設定済みの物として扱う

::

  $ cd kawaz3rd
  $ python manage.py syncdb
  $ python manage.py loaddata production
  $ python manage.py loaddata debug



2. `config.sample.ini`を`config.ini`にコピー
~~~~~~~~~

3. ドライバーの設定を以下のように変更
~~~~~~~~~~~~~~~~~~~

srcには2nd、dstには3rdを指定すべし

::

  [driver]
  src = mysql+pymysql://username:password@localhost/src_dbname?charset=utf8
  dst = mysql+pymysql://username:password@localhost/dst_dbname?charset=utf8
  

4. 実行
~~~~~~~~~~~~~~~~~

::
  
  $ cd ouroboros
  $ python converter.py


SQLite3（非推奨）
--------

1. 変換元のKawaz2のdbをdb/kawaz.dbとして保存
~~~~~~~~~~~~~~

2. Kawaz3rdでsyncdbしたDBをdb/kawaz3.dbとして保存
~~~~~~~~~~~~~~~

3. config.iniを設定
~~~~~~~~~~~~~~~~~

::

  [driver]
  src = sqlite:///db/kawaz.db
  dst = sqlite:///db/kawaz3.db


4. 以下のコマンドを実行
~~~~~~~~~~~~~~~~~~~~


::

  $ cd ouroboros
  $ python converter.py


処理の流れ
======================


1. Converter
------------------

2ndのテーブルから上手い具合に3rdのテーブルに写す。
カラムの追加削除や、初期値の設定もやってくれる

また、外部ファイルのパスの変換もやってくれます

- AnnouncementConverter
- AttachmentMaterialConverter
- BlogCategoryConverter
- BlogEntryConverter
- CommentConverter
- EventConverter
- EventAttendeeConverter
- PersonaConverter
- AccountConverter
- ProfileConverter
- ProfileSkillConverter
- ProjectConverter
- ProjectMemberConverter
- StarConverter

2. Processor
--------------------

写した後のデータの値をいじる処理。以下のProcessorが順に適応される

ContentTypeProcessor
~~~~~~~~~~~~~~~~~~~~~~

2ndと3rdのContentTypeテーブルを参照して変換表を作り、ContentTypeを参照している物をコンバートする

- Star
- Comment

あたりに適応される

AttachmentProcessor
~~~~~~~~~~~~~~~~~~~~~~

各本文中に含まれる素材埋め込みタグを新仕様に変換する

`{commons:1}`を`{attachments:123456789abcdef}`など


TimeZoneProcessor
~~~~~~~~~~~~~~~~~~~

2ndでは全てのdatetimeがJSTで保存されているが、3rdではUTCなので、タイムゾーンを変換する。

具体的には保存時刻を9時間戻している。

CodeBlockProcessor
~~~~~~~~~~~~~~~~~~~~

2ndのCodeBlock記法をKFMのFencedCodeBlockにコンバートします

~~~ -> ```
~~~.python -> ```
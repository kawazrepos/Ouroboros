Ouroboros
==============

Ouroboros is the database converter from Kawaz2 to Kawaz3.

必要環境
===================

- Python3.3++

セットアップ
====================

```sh
$ pip install -r requirements.txt
$ python converter.py
```

変換方法
====================

現段階ではSQLiteの変換を想定していますが、あとでMySQLにも対応させる予定

1. 変換元のKawaz2のdbをdb/kawaz.dbとして保存
2. Kawaz3rdでsyncdbしたDBをdb/kawaz3.dbとして保存
3. 以下のコマンドを実行

```sh
$ cd ouroboros
$ python converter.py
```

実行時オプション
======================


準備中
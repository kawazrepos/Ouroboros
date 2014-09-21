# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from ouroboros.utils.meta import copy_table, copy_column, deep_copy, set_schema_name
from sqlalchemy.schema import Column, Table, MetaData

class BaseConverter(object):
    """
    データ移行用のコンバーターです
    """
    # 移行元のテーブル名
    src_table_name = None

    # 移行先のテーブル名
    dst_table_name = None

    # 無視するカラム名
    exclude_columns = ()

    # 変更するカラムをtupleで渡す
    # (('before', 'after'), ())
    rename_columns = ()

    # 新しいカラムに与えるColumnのパラメータを指定できます
    # (('column_name': {'nullable': True}),)
    new_columns = ()

    # あるカラムの初期値を設定できます
    # 引数に定数血を入れた場合は自動的に定数値が設定されます
    # 引数にレコードを辞書で取る関数も渡せます
    # この引数はカラムのリネームと併用した場合、変更適用後のカラム名がキーになっています
    # (
    #   ('column0': 'default_value'),
    #   ('column1': lambda old_record: old_record['another_column']),
    # )
    default_values = ()


    def query(self, query):
        return query

    def table(self, table):
        return table

    def record(self, record):
        return record


class PortConverter(BaseConverter):

    def __init__(self, **kwargs):
        self.tables = kwargs['tables']
        self.dst_meta = kwargs['dst_meta']
        if not self.src_table_name:
            raise Exception("PortConverter must have `src_table_name`.")
        if not self.dst_table_name:
            # dst_table_nameが明示されてなかったら
            # src_table_nameにそのままコピーする
            self.dst_table_name = self.src_table_name

    def query(self, query):
        return query

    def table(self, table):
        # すでに定義済みのテーブルを読み込む
        return Table(self.dst_table_name, self.dst_meta, autoload=True)

    def record(self, record):
        new_records = {key: value for key, value in record.items() if not key in self.exclude_columns}
        for before, after in self.rename_columns:
            if before in new_records.keys():
                new_records[after] = new_records[before]
                del new_records[before]
        # デフォルト値の設定
        default_values_dict = dict(self.default_values)
        for k, v in default_values_dict.items():
            if callable(v):
                result = v(new_records)
                if result is None:
                    # NoneだったらNoneを返す
                    return None
                new_records[k] = result
            else:
                new_records[k] = v
        return new_records


class JoinConverter(PortConverter):
    right_table_name = None
    left_key = None
    right_key = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.right_table_name:
            raise Exception("JoinConverter must have 'right_table_name'.")
        if not self.left_key or not self.right_key:
            raise Exception("JoinConverter must have 'left/right_key'.")

    def query(self, query):
        right_table = self.tables[self.right_table_name]
        query = query.join(right_table, query.columns[self.left_key] == right_table.columns[self.right_key])
        return query

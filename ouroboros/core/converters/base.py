# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from ouroboros.utils.meta import copy_table, deep_copy, set_schema_name
from sqlalchemy.schema import Column, Table, MetaData

class BaseConverter(object):
    """
    データ移行用のコンバーターです
    """
    # 移行元のテーブル名
    src_table_name = None
    # 移行先のテーブル名
    dst_table_name = None
    # 無視するカラム
    exclude_columns = ()
    # 変更するカラムをtupleで渡す
    # (('before', 'after'), ())
    rename_columns = ()


    def __init__(self):
        if not self.src_table_name:
            raise Exception("Converter must have `src_table_name`.")
        if not self.dst_table_name:
            # dst_table_nameが明示されてなかったら
            # src_table_nameにそのままコピーする
            self.dst_table_name = self.src_table_name

    def query(self, query):
        return query

    def table(self, table):
        src_table = table
        new_table = Table(src_table.name, MetaData())
        rename_dict = dict(self.rename_columns)
        # 不要カラムの削除
        for c in src_table.columns:
            if c.name not in self.exclude_columns:
                copied_column = c.copy()
                if c.name in rename_dict.keys():
                    copied_column.name = rename_dict[c.name]
                new_table.append_column(copied_column)
        # dst_table_nameが別に設定されていたらリネーム
        if not self.src_table_name == self.dst_table_name:
            set_schema_name(new_table, self.dst_table_name)
        return new_table

    def record(self, record):
        new_records = {key: value for key, value in record.items() if not key in self.exclude_columns}
        # for before, after in self.rename_columns:
        #     if before in new_records.keys():
        #         new_records[after] = new_records[before]
        #         del new_records[before]
        return new_records

# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from ouroboros.utils.meta import copy_table, deep_copy, set_schema_name

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
        new_table = copy_table(table)
        # dst_table_nameが別に設定されていたらリネーム
        if not self.src_table_name == self.dst_table_name:
            set_schema_name(new_table, self.dst_table_name)
        return new_table

    def record(self, record):
        new_records = {key: value for key, value in record.items() if not key in self.exclude_columns}
        return new_records

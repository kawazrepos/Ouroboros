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
    # 無視するカラム
    exclude_columns = ()
    # 変更するカラムをtupleで渡す
    # (('before', 'after'), ())
    rename_columns = ()
    new_columns = ()
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

    def get_or_create_table(self, tablename):
        # if tablename in self.dst_meta.tables:
        #     return self.dst_meta.tables[tablename], False
        return Table(tablename, self.dst_meta), True

    def query(self, query):
        return query

    def table(self, table):
        src_table = table
        dst_table, created = self.get_or_create_table(self.dst_table_name)
        rename_dict = dict(self.rename_columns)
        # 不要カラムの削除
        for c in src_table.columns:
            if c.name not in self.exclude_columns:
                copied_column = c.copy()
                if c.name in rename_dict.keys():
                    copied_column.name = rename_dict[c.name]
                dst_table.append_column(copied_column)
        # dst_table_nameが別に設定されていたらリネーム
        if not self.src_table_name == self.dst_table_name:
            set_schema_name(dst_table, self.dst_table_name)
        # attributeを設定
        new_columns_dict = dict(self.new_columns)
        for column_name, options in new_columns_dict.items():
            if column_name in dst_table.c:
                column = dst_table.c[column_name]
                for k, v in options.items():
                    setattr(column, k, v)
        return dst_table

    def record(self, record):
        new_records = {key: value for key, value in record.items() if not key in self.exclude_columns}
        # for before, after in self.rename_columns:
        #     if before in new_records.keys():
        #         new_records[after] = new_records[before]
        # デフォルト値の設定
        default_values_dict = dict(self.default_values)
        for k, v in default_values_dict.items():
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
        return super().query(query)

    def table(self, table):
        left_table = table
        right_table = self.tables[self.right_table_name]

        dst_table, created = self.get_or_create_table(self.dst_table_name)

        for column in left_table.columns:
            dst_table.append_column(copy_column(column))

        for column in right_table.columns:
            dst_table.append_column(copy_column(column))
        return super().table(dst_table)

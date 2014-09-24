__author__ = 'tanix'

import copy
from sqlalchemy.schema import Column, Table, MetaData
from sqlalchemy.sql.elements import quoted_name

def copy_table(table):
    """
     渡されたテーブルをコピーします
    """
    ret_table = Table(table.name, MetaData())
    for c in table.columns:
        ret_table.append_column(copy_column(c))

    return ret_table

def copy_column(column):
    """
    渡されたカラムをコピーします
    """
    return Column(column.name, column.type)

def set_schema_name(s, name):
    s.name = quoted_name(name, s.kwargs.pop('quote', None))

def deep_copy(t):
    return copy.copy(t)


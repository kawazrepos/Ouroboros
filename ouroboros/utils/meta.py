__author__ = 'tanix'

import copy
from sqlalchemy.schema import Column, Table, MetaData
from sqlalchemy.sql.elements import quoted_name

def _copy_table(table):
    ret_table = Table(table.name, MetaData())
    for c in table.columns:
        ret_table.append_column(_copy_column(c))

    return ret_table

def _copy_column(column):
    return Column(column.name, column.type)

def _set_schema_name(s, name):
    s.name = quoted_name(name, s.kwargs.pop('quote', None))

def _copy(t):
    return copy.copy(t)

def id():
    def _(tables, src_tn):
        def _query(query):
            return query

        def _table(table):
            return _copy_table(table)

        def _record(record):
            return _copy(record)

        return {'query': _query, 'table': _table, 'record': _record}

    return _



def rename_table(dst_name):
    def _(tables, src_tn):
        def _query(query):
            return query

        def _table(table):
            t = _copy_table(table)
            _set_schema_name(t, dst_name)
            return t

        def _record(record):
            return _copy(record)

        return {'query': _query, 'table': _table, 'record': _record}

    return _



def exclude_columns(columns):
    def _(tables, src_tn):
        def _query(query):
            return query

        def _table(table):
            src_table = table
            new_table = Table(src_table.name, MetaData())

            for c in src_table.columns:
                if c.name not in columns:
                    new_table.append_column(c.copy())
            return new_table

        def _record(record):
            r = dict()
            for n in record.keys():
                if n not in columns:
                    r[n] = record[n]
            return r

        return {'query': _query, 'table': _table, 'record': _record}

    return _



def rename_columns(maps):
    src_columns = maps.keys()

    def _(tables, src_tn):
        def _query(query):
            return query

        def _table(table):
            src_table = table
            new_table = Table(src_table.name, MetaData())

            for c in src_table.columns:
                renamed_column = c.copy()
                if c.name in src_columns:
                    renamed_column.name = maps[c.name]
                new_table.append_column(renamed_column)

            return new_table

        def _record(record):
            r = dict()
            for n in record.keys():
                r[n] = record[n]

                # Bug?: SQLAlchemy raises an error in insertion of a record with renamed columns
                #if n in src_columns:
                #    r[maps[n]] = record[n]
                #else:
                #    r[n] = record[n]

            return r

        return {'query': _query, 'table': _table, 'record': _record}

    return _

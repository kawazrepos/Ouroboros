# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#
__author__ = 'giginet'

class BaseProcessor(object):
    # Processorを適応するテーブル.カラム
    # targets = ('table.column0',)
    targets = ()

    # Processorの名前
    name = 'BaseProcessor'

    def __init__(self, **kwargs):
        self.src_meta = kwargs['src_meta']
        self.dst_meta = kwargs['dst_meta']
        self.src_session = kwargs['src_session']
        self.dst_session = kwargs['dst_session']

    def _search_record(self, records, **kwargs):
        """
        レコードの辞書の一覧から条件に当てはまるモノを返す。見つからなかったらNone
        >>> self._search_record(records, id=10, name="hoge")
        """
        for r in records:
            for k, v in kwargs.items():
                if not r[k] == v:
                    break
                return r
        return None

    def _partial_update(self, table, record, column_name):
        query = {}
        query[column_name] = record[column_name]

        def get_pk(table):
            for c in table.c:
                if c.primary_key:
                    return c
            return None

        pk_column = get_pk(table)
        where = "{}=={}".format(pk_column.name, record[pk_column.name])

        update = table.update().where(where).values(query)
        self.dst_session.execute(update)

# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

class Migrator(object):

    def __init__(self, converters, src_path, dst_path):
        self.src_engine = create_engine(src_path)
        self.dst_engine = create_engine(dst_path, echo=True)

        self.converters = converters

    def migrate(self):
        src_meta = MetaData(bind=self.src_engine)
        src_meta.reflect()
        dst_meta = MetaData(bind=self.dst_engine)

        src_session = sessionmaker(bind=self.src_engine)()
        dst_session = sessionmaker(bind=self.dst_engine)()

        src_tables = src_meta.tables

        for src_tn in src_tables:
            if src_tn in self.converters:
                converter = partial(self._pipe_converters, src_tables, src_tn)
                get_query = converter('query')
                convert_table = converter('table')
                convert_record = converter('record')

                src_table = src_tables[src_tn]
                dst_table = convert_table(src_table).tometadata(dst_meta)
                dst_table.create()

                src_query = get_query(src_table).select()

                for r in src_session.query(src_query).all():
                    src_record = r._asdict()
                    dst_record = convert_record(src_record)
                    ins = dst_table.insert(values=dst_record)
                    dst_session.execute(ins)
                dst_session.commit()

    def _pipe_converters(self, tables, src_tn, key):
        def piped(x):
            r = x
            for o in self.converters[src_tn]:
                d = o(tables, src_tn)
                r = d[key](r)
            return r
        return piped


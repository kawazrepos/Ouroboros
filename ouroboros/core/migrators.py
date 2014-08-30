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
    """
    Kawaz2から3へのコンバーターです

    converters [ouroboros.core.converters.base.Converter] コンバータの一覧をtupleで渡します
    src_path: srcとなるDBのパスを追加します
    dst_path: 移行先のDBのパスを追加します
    """

    def __init__(self, converters, src_path, dst_path):
        self.src_engine = create_engine(src_path)
        self.dst_engine = create_engine(dst_path, echo=True)

        self.converters = converters

    def migrate(self):
        """
        マイグレーションを実行します
        """
        src_meta = MetaData(bind=self.src_engine)
        src_meta.reflect()
        dst_meta = MetaData(bind=self.dst_engine)

        src_session = sessionmaker(bind=self.src_engine)()
        dst_session = sessionmaker(bind=self.dst_engine)()

        src_tables = src_meta.tables

        for converter_cls in self.converters:
            converter = converter_cls()
            src_tn = converter.src_table_name
            if src_tn in src_tables:
                command_cls = converter.get_command_cls()
                command = command_cls(src_tables, src_tn)
                src_table = src_tables[src_tn]
                dst_table = command.table(src_table).tometadata(dst_meta)
                dst_table.create()

                src_query = command.query(src_table).select()

                for r in src_session.query(src_query).all():
                    src_record = r._asdict()
                    dst_record = command.record(src_record)
                    ins = dst_table.insert(values=dst_record)
                    dst_session.execute(ins)
                dst_session.commit()


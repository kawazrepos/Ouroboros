# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from ouroboros.core.processors import processors

class Migrator(object):
    """
    Kawaz2から3へのコンバーターです

    converters [ouroboros.core.converters.base.Converter] コンバータの一覧をtupleで渡します
    src_path: srcとなるDBのパスを追加します
    dst_path: 移行先のDBのパスを追加します
    """

    def __init__(self, converters, src_path, dst_path, config={}):
        self.config = config
        self.src_engine = create_engine(src_path)
        self.dst_engine = create_engine(dst_path, echo=self.config.get('verbose', False))

        self.converters = converters

    def migrate(self):
        """
        マイグレーションを実行します
        """
        src_meta = MetaData(bind=self.src_engine)
        src_meta.reflect()
        dst_meta = MetaData(bind=self.dst_engine)
        dst_meta.reflect()

        src_session = sessionmaker(bind=self.src_engine)()
        dst_session = sessionmaker(bind=self.dst_engine)()

        src_tables = src_meta.tables

        for converter_cls in self.converters:
            src_tn = converter_cls.src_table_name
            if src_tn in src_tables:
                converter = converter_cls(tables=src_tables, dst_meta=dst_meta)
                print("{} to {}".format(converter.src_table_name, converter.dst_table_name))
                src_table = src_tables[src_tn]
                dst_table = converter.table(src_table)
                dst_table.create(checkfirst=True)

                src_query = converter.query(src_table).select()
                dl = dst_table.delete()
                dst_session.execute(dl)
                dst_meta.reflect()

                q = src_session.query(src_query.alias("subquery1"))
                for r in q.all():
                    src_record = r._asdict()
                    dst_record = converter.record(src_record)

                    if dst_record: # Noneが返ってきたら無視する
                        ins = dst_table.insert().values(dst_record)
                        dst_session.execute(ins)
                dst_session.commit()
            else:
                print("Source table {} is not found".format(src_tn))

        # プロセッサーで処理をする
        for processor_cls in processors:
            print("Process of {}".format(processor_cls.name))
            processor = processor_cls(src_session=src_session,
                                      src_meta=src_meta,
                                      dst_session=dst_session,
                                      dst_meta=dst_meta)
            processor.convert()


# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from ouroboros.utils.meta import copy_table
from ouroboros.core.converters.commands.base import BaseCommand

class BaseConverter(object):
    """
    データ移行用のコンバーターです
    """
    # 移行元のテーブル名
    src_table_name = None
    # 移行先のテーブル名
    dst_table_name = None
    # 消去用カラム
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

    def convert(self, table):
        pass

    def get_command_cls(self):
        # 恒久的にBaseCommandクラスを返す
        return BaseCommand

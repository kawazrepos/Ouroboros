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

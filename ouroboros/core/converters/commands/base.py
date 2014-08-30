# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from ouroboros.utils.meta import copy_table, deep_copy

class BaseCommand(object):

    def __init__(self, tables, src_table_name):
        self.tables = tables
        self.src_table_name = src_table_name

    def query(self, query):
        return query

    def table(self, table):
        return copy_table(table)

    def record(self, record):
        return deep_copy(record)
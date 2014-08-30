# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'

from .base import BaseConverter

"""単純に写すだけのスキーマです"""

class AuthGroupConverter(BaseConverter):
    src_table_name = 'auth_group'
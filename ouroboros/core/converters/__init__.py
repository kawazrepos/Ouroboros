# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'
from .base import BaseConverter

class AnnouncementConverter(BaseConverter):
    src_table_name = 'announcements_announcement'
    exclude_columns = (
        '_body_rendered',
        'sage',
        'updated_by_id',
        'publish_at',
        'publish_at_date',
        'body_markup_type'
    )


converters = (
    AnnouncementConverter,
)
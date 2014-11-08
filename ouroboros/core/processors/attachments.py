# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#
__author__ = 'giginet'

import re
from .base import BaseProcessor

COMMONS_PATTERN = re.compile(r"\{commons:\W*(?P<object_id>[^}:]+)(?P<size>[\w,]*)\W*\}", re.MULTILINE)
ATTACHMENT_PATTERN = "{attachments:%s}"

class AttachmentProcessor(BaseProcessor):
    """
    本文中の{commons:n}みたいな記法による素材埋め込みを
    Kawaz3rdの記法にコンバートするプロセッサーです
    """
    name = "AttachmentProcessor"
    targets = (
        'announcements_announcement.body',
        'blogs_entry.body',
        'django_comments.comment',
        'events_event.body',
        'personas_profile.remarks',
        'projects_project.body',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 予め、移行後のattachments_materialのレコードを全て辞書化しておく
        attachment_table = self.dst_meta.tables['attachments_material']
        self.attachment_records = [r._asdict() for r in self.dst_session.query(attachment_table.select().alias('subquery1')).all()]

    def convert(self):
        for target in self.targets:
            table_name, column_name = target.split('.')
            print("Convert attachment tag of {} in {}".format(column_name, table_name))
            table = self.dst_meta.tables[table_name]

            for r in self.dst_session.query(table.select().alias('subquery1')).all():
                record = r._asdict()
                src_body = record[column_name]
                def repl(m):
                    # {commons:number}のnumberの部分を取得
                    commons_id = m.group('object_id')
                    # 対象となるMaterialを取得
                    material = self._search_record(self.attachment_records, id=int(commons_id))
                    if material:
                        slug = material['slug']
                        # {attachment:slug}みたいな奴に差し替える
                        return ATTACHMENT_PATTERN % (slug,)
                    return m.group()

                dst_body = re.sub(COMMONS_PATTERN, repl, src_body)
                record[column_name] = dst_body
                self._partial_update(table, record, column_name)

        self.dst_session.commit()

import re
from ouroboros.core.processors.base import BaseProcessor

__author__ = 'giginet'

class CodeBlockProcessor(BaseProcessor):
    """
    本文中のコードブロック記法をKFM（KawazFlavoredMarkdown）向けのFencedCodeBlockにコンバートします

    ~~~ -> ```
    ~~~.python -> ```python
    """
    CODEBLOCK_PATTERN = r'''~{3}\.?'''
    name = "CodeBlockProcessor"
    targets = (
        'announcements_announcement.body',
        'blogs_entry.body',
        'django_comments.comment',
        'events_event.body',
        'personas_profile.remarks',
        'projects_project.body',
    )

    def convert(self):
        for target in self.targets:
            table_name, column_name = target.split('.')
            print("Convert code block syntax of {} in {}".format(column_name, table_name))
            table = self.dst_meta.tables[table_name]

            for r in self.dst_session.query(table.select().alias('subquery1')).all():
                record = r._asdict()
                src_body = record[column_name]
                dst_body = re.sub(self.CODEBLOCK_PATTERN, '```', src_body)
                record[column_name] = dst_body
                self._partial_update(table, record, column_name)
        self.dst_session.commit()

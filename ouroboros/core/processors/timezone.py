import pytz
import datetime
from ouroboros.core.processors.base import BaseProcessor

__author__ = 'giginet'

FORMAT = '%Y-%m-%d %X'

class TimeZoneProcessor(BaseProcessor):
    """
    JSTで格納されていたdatetimeをUTCに変換するプロセッサーです
    """

    name = 'TimeZoneProcessor'

    targets = (
        'announcements_announcement.created_at',
        'announcements_announcement.updated_at',
        'attachments_material.created_at',
        'blogs_entry.created_at',
        'blogs_entry.updated_at',
        'blogs_entry.publish_at',
        'django_comments.submit_date',
        'events_event.created_at',
        'events_event.updated_at',
        'events_event.period_start',
        'events_event.period_end',
        'personas_persona.date_joined',
        'personas_profile.created_at',
        'personas_profile.updated_at',
        'projects_project.created_at',
        'projects_project.updated_at',
        'stars_star.created_at',
    )

    def convert(self):
        jst = pytz.timezone('Asia/Tokyo')
        for target in self.targets:
            table_name, column_name = target.split('.')
            print("Convert timezone of {} in {}".format(column_name, table_name))
            table = self.dst_meta.tables[table_name]
            for r in self.dst_session.query(table.select().alias('subquery1')).all():
                record = r._asdict()
                src_datetime = record[column_name]
                if src_datetime:
                    aware_src = jst.localize(src_datetime)
                    dst_datetime = aware_src.astimezone(pytz.UTC)
                    record[column_name] = dst_datetime.strftime(FORMAT)
                    self._partial_update(table, record, column_name)

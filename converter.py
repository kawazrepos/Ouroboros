from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from ouroboros.utils.meta import id, rename_table, exclude_columns, rename_columns

converters = {
    'auth_group': [id()],
    'blogs_category': [id()],
    'commons_material': [id()],
    'django_flatpage': [id()],
    'django_flatpage_sites': [id()],
    'django_site': [id()],
    'profiles_skill': [id()],
    'projects_category': [id()],
    'tagging_tag': [id()],
    'blogs_entry': [id()],

    'auth_user': [rename_table('personas_persona')],

    'events_event_members': [rename_table('events_event_attendees'),
                             rename_columns({'user_id': 'persona_id'})],

    'announcements_announcement': [exclude_columns(['updated_by_id',
                                                    'publish_at',
                                                    'publish_at_date']),
                                   rename_columns({'sage': 'silently'})],
    'events_event': [exclude_columns(['publish_at', 'publish_at_date'])],

    'projects_project': [exclude_columns(['updated_by_id',
                                          'publish_at',
                                          'publish_at_date',
                                          'bugwaz_id',
                                          'permission']),
                         rename_columns({'author_id': 'administrator_id'})],

    'projects_project_members': [rename_columns({'user_id': 'persona_id'})],

    'profiles_profile_skills': [rename_columns({'user_id': 'persona_id'})],

    'star_star': [rename_table('stars_star'),
                  rename_columns({'comment': 'quotes'}),
                  exclude_columns(['tag'])]
}

def pipe_functions(dic, key):
    def piped(x):
        r = x
        for d in dic:
            r = d[key](r)
        return r

    return piped


if __name__ == '__main__':

    src_engine = create_engine('sqlite:///db/kawaz.db')
    dst_engine = create_engine('sqlite:///db/kawaz3.db', echo=True)

    src_meta = MetaData(bind=src_engine)
    src_meta.reflect()
    dst_meta = MetaData(bind=dst_engine)

    src_session = sessionmaker(bind=src_engine)()
    dst_session = sessionmaker(bind=dst_engine)()

    for src_tn in src_meta.tables:
        src_table = src_meta.tables[src_tn]
        if src_tn in converters:
            schema_convert = pipe_functions(converters[src_tn], 'table')
            dst_table = schema_convert(src_table).tometadata(dst_meta)
            dst_table.create()
            dst_session.commit()
            for r in src_session.query(src_table).all():
                src_record = r._asdict()
                record_convert = pipe_functions(converters[src_tn], 'record')
                dst_record = record_convert(src_record)
                ins = dst_table.insert(values=dst_record)
                dst_session.execute(ins)
            dst_session.commit()

from ouroboros.utils.meta import id, rename_table, exclude_columns, rename_columns, join_tables
from ouroboros.core.migrators import Migrator

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

    'auth_user': [join_tables('profiles_profile', 'id', 'user_id'),
                  rename_table('personas_persona'),
                  rename_columns({'icon': 'avator',
                                  'sex': 'gender',
                                  'mood': 'quotes'}),
                  exclude_columns(['pub_state',
                                   'birthday',
                                   'place',
                                   'location',
                                   'url',
                                   'remarks',
                                   'remarks_markup_type',
                                   'user_id',
                                   '_remarks_rendered',
                                   'twitter_token',
                                   'created_at',
                                   'updated_at'])],

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

from ouroboros.core.converters.moves import AuthGroupConverter

if __name__ == '__main__':
    migrator = Migrator((AuthGroupConverter,), 'sqlite:///db/kawaz.db', 'sqlite:///db/kawaz3.db')
    migrator.migrate()
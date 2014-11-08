# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'
import re
from .base import PortConverter
from .base import JoinConverter

class AnnouncementConverter(PortConverter):
    src_table_name = 'announcements_announcement'
    exclude_columns = (
        '_body_rendered',
        'sage',
        'updated_by_id',
        'publish_at',
        'publish_at_date',
        'body_markup_type'
    )

    def convert_last_modifier(record):
        return record['author_id']

    default_values = (
        ('last_modifier_id', convert_last_modifier),
    )


class AttachmentMaterialConverter(PortConverter):
    src_table_name = 'commons_material'
    dst_table_name = 'attachments_material'
    rename_columns = (
        ('file', 'content_file'),
    )
    exclude_columns = (
        'pub_state',
        'license',
        'title',
        'body',
        'project_id',
        'pv',
        'updated_at'
    )

    def convert_content_file_path(record):
        path = record['content_file']
        return re.sub("storage/commons/(?P<path>.+)", "attachments/\g<path>", path)

    def convert_slug(record):
        path = record['content_file']
        # こっちでもコンバートする
        converted = re.sub("storage/commons/(?P<path>.+)", "attachments/\g<path>", path)
        import hashlib
        # sha1でハッシュ化
        return hashlib.sha1(converted.encode('utf-8')).hexdigest()

    default_values = (
        ('slug', convert_slug),
        ('content_file', convert_content_file_path)
    )


class BlogCategoryConverter(PortConverter):
    src_table_name = 'blogs_category'


class BlogEntryConverter(PortConverter):
    src_table_name = 'blogs_entry'
    exclude_columns = (
        'body_markup_type',
        '_body_rendered',
        'publish_at_date'
    )


class CommentConverter(PortConverter):
    src_table_name = 'mcomments_markitupcomment'
    dst_table_name = 'django_comments'
    exclude_columns = (
        '_comment_rendered',
        'comment_markup_type'
    )


class EventConverter(PortConverter):
    src_table_name = 'events_event'
    exclude_columns = (
        'location',
        'body_markup_type',
        '_body_rendered',
        'publish_at',
        'publish_at_date',
        'gcal'
    )
    rename_columns = (
        ('author_id', 'organizer_id'),
    )


class EventAttendeeConverter(PortConverter):
    src_table_name = 'events_event_members'
    dst_table_name = 'events_event_attendees'
    rename_columns = (
        ('user_id', 'persona_id'),
    )

profile_deprecated_columns = (
        'location',
        'twitter_token',
        'remarks_markup_type',
        '_remarks_rendered',
    )

class PersonaConverter(JoinConverter):
    src_table_name = 'profiles_profile'
    right_table_name = 'auth_user'
    left_key = 'user_id'
    right_key = 'id'
    dst_table_name = 'personas_persona'
    rename_columns = (
        ('mood', 'quotes'),
        ('icon', 'avatar'),
        ('sex', 'gender')
    )
    exclude_columns = list(profile_deprecated_columns) + [
        'pub_state',
        'birthday',
        'place',
        'url',
        'remarks',
        'user_id',
        'created_at',
        'updated_at',
        'is_superuser',
        'is_staff'
    ]

    def convert_avatar_path(record):
        path = record['avatar']
        return re.sub("storage/(?P<path>profiles/.+)", "\g<path>", path)

    def convert_nickname(record):
        if 'nickname' in record:
            return record['nickname']
        return record['username']

    def convert_role(record):
        gods = ['giginet', 'miiojp', 'lambdalisue', 'shinka_cb', 'c000',]
        if 'username' in record:
            if record['username'] in gods:
                return 'seele'
        return 'children'

    def convert_gender(record):
        if 'gender' in record:
            if record['gender']:
                return record['gender']
        return 'unknown'

    default_values = (
        ('role', convert_role),
        ('avatar', convert_avatar_path),
        ('nickname', convert_nickname),
        ('gender', convert_gender)
    )


class AccountConverter(PortConverter):
    src_table_name = 'profiles_service'
    dst_table_name = 'personas_account'
    rename_columns = (
        ('account', 'username'),
        ('service', 'service_id'),
    )

    def convert_service_id(record):
        convert_dict = {
            "skype": 2,
            "twitter": 1,
            "mixi": 17,
            "facebook": 3,
            "foursquare": 4,
            "google": 5,
            "pixiv": 6,
            "hatena": 7,
            "xbl": 9,
            "psn": 10,
            "dropbox": 8
        }
        service_name = record['service_id']
        if service_name in convert_dict:
            return convert_dict[service_name]
        print("service name {} is invalid.".format(service_name))
        return None

    default_values = (
        ('service_id', convert_service_id),
    )


class ProfileConverter(PortConverter):
    src_table_name = 'profiles_profile'
    dst_table_name = 'personas_profile'
    exclude_columns = list(profile_deprecated_columns) + [
        'nickname',
        'mood',
        'icon',
        'sex'
    ]


class ProfileSkillConverter(PortConverter):
    src_table_name = 'profiles_profile_skills'
    dst_table_name = 'personas_profile_skills'


class ProjectConverter(PortConverter):
    # Add tracker, repository
    src_table_name = 'projects_project'
    exclude_columns = (
        'permission',
        'body_markup_type',
        '_body_rendered',
        'updated_by_id',
        'group_id',
        'publish_at',
        'publish_at_date',
        'bugwaz_id'
    )
    rename_columns = (
        ('author_id', 'administrator_id'),
    )

    def convert_icon_path(record):
        path = record['icon']
        return re.sub("storage/(?P<path>projects/.+)", "\g<path>", path)

    def convert_last_modifier(record):
        return record['administrator_id']

    default_values = (
        ('repository', ''),
        ('tracker', ''),
        ('icon', convert_icon_path),
        ('last_modifier_id', convert_last_modifier),
    )

class ProjectMemberConverter(PortConverter):
    src_table_name = 'projects_project_members'
    rename_columns =  (
        ('user_id', 'persona_id'),
    )

class StarConverter(PortConverter):
    src_table_name = 'star_star'
    dst_table_name = 'stars_star'
    rename_columns = (
        ('comment', 'quote'),
    )
    exclude_columns = (
        'tag',
    )


converters = (
    AnnouncementConverter,
    AttachmentMaterialConverter,
    BlogCategoryConverter,
    BlogEntryConverter,
    CommentConverter,
    EventConverter,
    EventAttendeeConverter,
    PersonaConverter,
    AccountConverter,
    ProfileConverter,
    ProfileSkillConverter,
    ProjectConverter,
    ProjectMemberConverter,
    StarConverter,
)

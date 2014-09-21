# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/30
#
__author__ = 'giginet'
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
    default_values = (
        ('slug', lambda record: record['content_file']),
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
    src_table_name = 'auth_user'
    right_table_name = 'profiles_profile'
    left_key = 'id'
    right_key = 'user_id'
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


class AccountConverter(PortConverter):
    src_table_name = 'profiles_service'
    dst_table_name = 'profiles_account'


class ProfileConverter(PortConverter):
    src_table_name = 'profiles_profile'
    rename_columns = (
        ('user_id', 'id'),
    )
    exclude_columns = list(profile_deprecated_columns) + [
        'nickname',
        'mood',
        'icon',
        'sex'
    ]


class ProfileSkillConverter(PortConverter):
    src_table_name = 'profiles_profile_skills'


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
    default_values = (
        ('repository', ''),
        ('tracker', ''),
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
    # PersonaConverter,
    AccountConverter,
    # ProfileConverter,
    ProfileSkillConverter,
    ProjectConverter,
    ProjectMemberConverter,
    StarConverter,
)
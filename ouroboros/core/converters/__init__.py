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


class AttachmentMaterialConverter(BaseConverter):
    src_table_name = 'commons_material'
    dst_table_name = 'attachments_material'
    exclude_columns = (
        'pub_state',
        'license',
        'title',
        'body',
        'project_id',
        'pv',
        'update_at'
    )


class BlogCategoryConverter(BaseConverter):
    src_table_name = 'blogs_category'


class BlogEntryConverter(BaseConverter):
    src_table_name = 'blogs_entry'
    exclude_columns = (
        'body_markup_type',
        '_body_rendered',
        'publish_at_date'
    )


class CommentConverter(BaseConverter):
    src_table_name = 'mcomments_markitupcomment'
    dst_table_name = 'django_comments'
    exclude_columns = (
        '_comment_rendered',
        'comment_markup_type'
    )


class EventConverter(BaseConverter):
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


class EventAttendeeConverter(BaseConverter):
    src_table_name = 'events_event_attendees'
    dst_table_name = 'events_event_members'
    rename_columns = (
        ('user_id', 'persona_id'),
    )


class PersonaConverter(BaseConverter):
    src_table_name = 'profiles_profile'
    dst_table_name = 'personas_persona'
    rename_columns = (
        ('mood', 'quotes'),
        ('icon', 'avatar'),
        ('sex', 'gender')
    )


class AccountConverter(BaseConverter):
    src_table_name = 'profiles_service'
    dst_table_name = 'profiles_account'


class ProfileConverter(BaseConverter):
    src_table_name = 'profiles_profile'
    exclude_columns = (
        'nickname',
        'mood',
        'icon',
        'sex',
        'location',
        'twitter_token'
    )


class ProfileSkillConverter(BaseConverter):
    src_table_name = 'profiles_profile_skills'


class ProjectConverter(BaseConverter):
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

class ProjectMemberConverter(BaseConverter):
    src_table_name = 'projects_project_members'
    rename_columns =  (
        ('user_id', 'persona_id'),
    )

class StarConverter(BaseConverter):
    src_table_name = 'star_star'
    dst_table_name = 'stars_star'
    rename_columns = (
        ('comment', 'quote'),
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
    StarConverter
)
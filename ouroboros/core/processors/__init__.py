# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#
__author__ = 'giginet'

from ouroboros.core.processors.codeblock import CodeBlockProcessor
from ouroboros.core.processors.timezone import TimeZoneProcessor
from .content_types import ContentTypeProcessor
from .attachments import AttachmentProcessor

processors = (
    ContentTypeProcessor,
    AttachmentProcessor,
    TimeZoneProcessor,
    CodeBlockProcessor,
)
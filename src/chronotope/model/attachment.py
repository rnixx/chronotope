from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Sequence,
)
from sqlalchemy.orm import mapper
from pyramid.i18n import TranslationStringFactory
from ..sql import (
    get_session,
    metadata,
    SQLRowNodeAttributes,
    SQLRowNode,
)


_ = TranslationStringFactory('chronotope')


attachment_table = Table('attachment', metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', String(36)),
    Column('creator', String(80)),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('title', String(255)),
    #Column('attachment_type, ...
    #Column('payload, ...
)


class Attachment(object):

    def __init__(self, uid, creator, created, modified, title,
                 attachment_type, payload):
        self.uid = uid
        self.creator = creator
        self.created = created
        self.modified = modified
        self.title = title
        self.attachment_type = attachment_type
        self.payload = payload


mapper(Attachment, attachment_table)

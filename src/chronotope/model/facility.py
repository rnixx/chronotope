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


facility_table = Table('facility', metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', String(36)),
    Column('creator', String(80)),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('exists_from', DateTime()),
    Column('exists_to', DateTime()),
    #Column('category, ...
    #Column('location, ...
)


class Facility(object):

    def __init__(self, uid, creator, created, modified, title, description,
                 exists_from, exists_to, category, location):
        self.uid = uid
        self.creator = creator
        self.created = created
        self.modified = modified
        self.title = title
        self.description = description
        self.exists_from = exists_from
        self.exists_to = exists_to
        self.category = category
        self.location = location


mapper(Facility, facility_table)

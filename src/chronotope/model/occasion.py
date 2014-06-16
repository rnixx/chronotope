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


occasion_table = Table('occation', metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', String(36)),
    Column('creator', String(80)),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('duration_from', DateTime()),
    Column('duration_to', DateTime()),
    #Column('facility, ...
)


class Occation(object):

    def __init__(self, uid, creator, created, modified, title, description,
                 duration_from, duration_to, facility):
        self.uid = uid
        self.creator = creator
        self.created = created
        self.modified = modified
        self.title = title
        self.description = description
        self.exists_from = duration_from
        self.exists_to = duration_to
        self.facility = facility


mapper(Occation, occasion_table)

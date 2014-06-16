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


location_table = Table('location', metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', String(36)),
    Column('creator', String(80)),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('lat', Float()),
    Column('lon', Float()),
    Column('street', String(120)),
    Column('zip', String(10)),
    Column('city', String(80)),
    Column('country', String(2)),
)


class Location(object):

    def __init__(self, uid, creator, created, modified,
                 lat, lon, street, zip, city, country):
        self.uid = uid
        self.creator = creator
        self.created = created
        self.modified = modified
        self.lat = lat
        self.lon = lon
        self.street = street
        self.zip = zip
        self.city = city
        self.country = country


mapper(Location, location_table)

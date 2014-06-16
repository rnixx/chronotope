from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
)
from pyramid.i18n import TranslationStringFactory
from ..sql import Base


_ = TranslationStringFactory('chronotope')


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    street = Column(String)
    zip = Column(String)
    city = Column(String)
    country = Column(String)

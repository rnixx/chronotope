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


class Occasion(Base):
    __tablename__ = 'occasion'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    description = Column(String)
    duration_from = Column(DateTime)
    duration_to = Column(DateTime)
    #facility = Column()

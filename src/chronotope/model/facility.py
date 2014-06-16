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


class Facility(Base):
    __tablename__ = 'facility'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    description = Column(String)
    exists_from = Column(DateTime)
    exists_to = Column(DateTime)
    #category = Column()
    #location = Column()

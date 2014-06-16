from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from pyramid.i18n import TranslationStringFactory
from ..sql import Base


_ = TranslationStringFactory('chronotope')


facility_location_references = Table(
        'facility_location_references', Base.metadata,
    Column('facility_id', Integer, ForeignKey('facility.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)


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
    location = relationship(
        "Location",
        secondary=facility_location_references,
        backref="parents")

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


occasion_facility_references = Table(
        'occasion_facility_references', Base.metadata,
    Column('occasion_id', Integer, ForeignKey('occasion.id')),
    Column('facility_id', Integer, ForeignKey('facility.id'))
)


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
    facility = relationship(
        "Facility",
        secondary=occasion_facility_references,
        backref="parents")

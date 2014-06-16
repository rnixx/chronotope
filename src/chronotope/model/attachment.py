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


attachment_location_references = Table(
        'attachment_location_references', Base.metadata,
    Column('attachment_id', Integer, ForeignKey('attachment.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)


attachment_facility_references = Table(
        'attachment_facility_references', Base.metadata,
    Column('attachment_id', Integer, ForeignKey('attachment.id')),
    Column('facility_id', Integer, ForeignKey('facility.id'))
)


class Attachment(Base):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    #attachment_type = Column()
    #payload = Column()
    location = relationship(
        "Location",
        secondary=attachment_location_references,
        backref="parents")
    facility = relationship(
        "Facility",
        secondary=attachment_facility_references,
        backref="parents")

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

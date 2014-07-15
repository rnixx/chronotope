from sqlalchemy import (
    Column,
    String,
)
from pyramid.i18n import TranslationStringFactory
from chronotope.sql import (
    GUID,
    SQLBase,
)


_ = TranslationStringFactory('chronotope')


class CategoryRecord(SQLBase):
    __tablename__ = 'category'
    uid = Column(GUID, primary_key=True)
    name = Column(String)

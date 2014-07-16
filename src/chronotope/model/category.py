import uuid
from sqlalchemy import (
    Column,
    String,
)
from pyramid.i18n import TranslationStringFactory
from chronotope.sql import (
    GUID,
    SQLBase,
    get_session,
)
from chronotope.utils import ensure_uuid


_ = TranslationStringFactory('chronotope')


class CategoryRecord(SQLBase):
    __tablename__ = 'category'
    uid = Column(GUID, primary_key=True)
    name = Column(String)


def add_category(request, name):
    session = get_session(request)
    category = CategoryRecord()
    category.uid = uuid.uuid4()
    category.name = name
    session.add(category)
    return category


def delete_category(request, category):
    session = get_session(request)
    session.delete(category)


def category_by_uid(request, uid):
    session = get_session(request)
    return session.query(CategoryRecord).get(ensure_uuid(uid))


def category_by_name(request, name):
    session = get_session(request)
    res = session.query(CategoryRecord).filter(CategoryRecord.name==name).all()
    if res:
        return res[0]


def categories_by_uid(request, uids):
    if not uids:
        return list()
    uids = [ensure_uuid(uid) for uid in uids]
    session = get_session(request)
    return session.query(CategoryRecord)\
                  .filter(CategoryRecord.uid.in_(uids))\
                  .all()


def search_categories(request, term, limit=None):
    session = get_session(request)
    query = session.query(CategoryRecord)\
                   .filter(CategoryRecord.name.like('%{0}%'.format(term)))\
                   .order_by(CategoryRecord.name)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

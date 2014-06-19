chronotope.model.category
=========================

::

    >>> import uuid
    >>> from chronotope.model import CategoryRecord
    >>> from chronotope.sql import get_session

    >>> request = layer.new_request()
    >>> session = get_session(request)

    >>> category1 = CategoryRecord()
    >>> category1.uid = uuid.UUID('9fede645-ede9-4768-92c4-ef051340c953')
    >>> category1.name = 'Category 1'
    >>> session.add(category1)

    >>> category2 = CategoryRecord()
    >>> category2.uid = uuid.UUID('9a66218c-7991-43e5-b6c2-be98268f5f75')
    >>> category2.name = 'Category 2'
    >>> session.add(category2)

    >>> session.commit()

    >>> res = session.query(CategoryRecord).all()
    >>> res
    [<chronotope.model.category.CategoryRecord object at ...>, 
    <chronotope.model.category.CategoryRecord object at ...>]

    >>> category = res[0]
    >>> category.uid
    UUID('9fede645-ede9-4768-92c4-ef051340c953')

    >>> category.name
    u'Category 1'

    >>> category.facility
    []

    >>> session.delete(category1)
    >>> session.delete(category2)
    >>> session.commit()

    >>> session.query(CategoryRecord).all()
    []

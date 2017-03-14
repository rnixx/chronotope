chronotope.model.category
=========================

Direct SQLA::

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

API::

    >>> from chronotope.model.category import add_category
    >>> from chronotope.model.category import delete_category
    >>> from chronotope.model.category import category_by_uid
    >>> from chronotope.model.category import categories_by_uid
    >>> from chronotope.model.category import category_by_name
    >>> from chronotope.model.category import search_categories

    >>> cat_1 = add_category(request, 'Cat 1')
    >>> cat_2 = add_category(request, 'Cat 2')
    >>> cat_3 = add_category(request, 'Cat 3')
    >>> session.commit()

    >>> category_by_uid(request, cat_1.uid)
    <chronotope.model.category.CategoryRecord object at ...>

    >>> category_by_uid(request, str(cat_1.uid))
    <chronotope.model.category.CategoryRecord object at ...>

    >>> category_by_uid(request, '9fede645-ede9-4768-92c4-ef051340c953')

    >>> categories_by_uid(request, [cat_1.uid, str(cat_2.uid)])
    [<chronotope.model.category.CategoryRecord object at ...>,
    <chronotope.model.category.CategoryRecord object at ...>]

    >>> categories_by_uid(request, ['9fede645-ede9-4768-92c4-ef051340c953'])
    []

    >>> category_by_name(request, 'Inexistent')

    >>> category_by_name(request, 'Cat 1')
    <chronotope.model.category.CategoryRecord object at ...>

    >>> search_categories(request, 'at')
    [<chronotope.model.category.CategoryRecord object at ...>,
    <chronotope.model.category.CategoryRecord object at ...>,
    <chronotope.model.category.CategoryRecord object at ...>]

    >>> search_categories(request, 'Cat', limit=2)
    [<chronotope.model.category.CategoryRecord object at ...>, 
    <chronotope.model.category.CategoryRecord object at ...>]

    >>> search_categories(request, 'Cat 1')
    [<chronotope.model.category.CategoryRecord object at ...>]

    >>> delete_category(request, cat_1)
    >>> delete_category(request, cat_2)
    >>> delete_category(request, cat_3)

    >>> session.commit()

    >>> session.query(CategoryRecord).all()
    []

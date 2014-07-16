chronotope.browser.category
===========================

Imports::

    >>> from cone.app import get_root
    >>> from chronotope.sql import get_session
    >>> from chronotope.model.category import (
    ...     add_category,
    ...     CategoryRecord,
    ... )
    >>> from chronotope.browser.category import json_category

Dummy data::

    >>> request = layer.new_request()
    >>> cat_1 = add_category(request, 'Cat 1')
    >>> cat_2 = add_category(request, 'Cat 2')
    >>> cat_3 = add_category(request, 'Cat 3')

Json view::

    >>> model = get_root()
    >>> request.params['q'] = 'Cat'
    >>> json_category(model, request)
    [{'text': 'Cat 1', 'id': '...'}, 
    {'text': 'Cat 2', 'id': '...'}, 
    {'text': 'Cat 3', 'id': '...'}]

    >>> request.params['q'] = 'Cat 1'
    >>> json_category(model, request)
    [{'text': 'Cat 1', 'id': '...'}]

    >>> request.params['q'] = 'Cat 4'
    >>> json_category(model, request)
    [{'text': 'Cat 4', 'id': 'Cat 4'}]

    >>> request.params['q'] = 'Cat,4'
    >>> json_category(model, request)
    [{'text': 'Cat 4', 'id': 'Cat 4'}]

Cleanup::

    >>> session = get_session(request)

    >>> session.delete(cat_1)
    >>> session.delete(cat_2)
    >>> session.delete(cat_3)
    >>> session.commit()

    >>> session.query(CategoryRecord).all()
    []

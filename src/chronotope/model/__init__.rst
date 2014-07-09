chronotope.model
================

Chronotope entry nodes::

    >>> from cone.app import get_root
    >>> root = get_root()

    >>> root.keys()
    ['settings', 'locations', 'facilities', 'occasions', 'attachments']

    >>> root['locations']
    <Locations object 'locations' at ...>

    >>> root['facilities']
    <Facilities object 'facilities' at ...>

    >>> root['occasions']
    <Occasions object 'occasions' at ...>

    >>> root['attachments']
    <Attachments object 'attachments' at ...>

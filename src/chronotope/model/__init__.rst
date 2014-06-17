chronotope.model
================

Chronotope node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> chronotope
    <Chronotope object 'chronotope' at ...>

Chronotope props::

    >>> props = chronotope.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.in_navtree
    True

    >>> props.icon
    'icon-globe'

Chronotope metadata::

    >>> md = chronotope.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'chronotope_label'

    >>> md.description
    u'chronotope_description'

Chronotope children::

    >>> chronotope.keys()
    ['locations', 'facilities', 'occasions', 'attachments']

    >>> chronotope['locations']
    <Locations object 'locations' at ...>

    >>> chronotope['facilities']
    <Facilities object 'facilities' at ...>

    >>> chronotope['occasions']
    <Occasions object 'occasions' at ...>

    >>> chronotope['attachments']
    <Attachments object 'attachments' at ...>

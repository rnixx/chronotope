chronotope.model.location
=========================

Locations node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> locations = chronotope['locations']
    >>> locations
    <Locations object 'locations' at ...>

    >>> locations.__parent__
    <Chronotope object 'chronotope' at ...>

Locations props::

    >>> props = locations.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.in_navtree
    True

    >>> props.action_up
    True

    >>> props.action_up_tile
    'content'

    >>> props.action_add
    True

    >>> props.default_content_tile
    'listing'

Locations metadata::

    >>> md = locations.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'locations_label'

    >>> md.description
    u'locations_description'

``__setitem__`` is not implemented::

    >>> locations['1'] = object()
    Traceback (most recent call last):
      ...
    NotImplementedError: ``__setitem__`` is not implemented.

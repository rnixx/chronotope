chronotope.model.location
=========================

Locations
---------

Locations node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> locations = chronotope['locations']
    >>> locations
    <Locations object 'locations' at ...>

Locations props::

    >>> props = locations.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.in_navtree
    True

    >>> props.action_up
    True

    >>> props.action_add
    True

Locations metadata::

    >>> md = locations.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'locations_label'

    >>> md.description
    u'locations_description'

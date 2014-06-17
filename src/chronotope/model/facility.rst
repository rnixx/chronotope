chronotope.model.facility
=========================

Facilities
----------

Facilities node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> facilities = chronotope['facilities']
    >>> facilities
    <Facilities object 'facilities' at ...>

Facilities props::

    >>> props = facilities.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.in_navtree
    True

    >>> props.action_up
    True

    >>> props.action_add
    True

Facilities metadata::

    >>> md = facilities.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'facilities_label'

    >>> md.description
    u'facilities_description'

chronotope.model.occasion
=========================

Occasions
---------

Occasions node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> occasions = chronotope['occasions']
    >>> occasions
    <Occasions object 'occasions' at ...>

Occasions props::

    >>> props = occasions.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.in_navtree
    True

    >>> props.action_up
    True

    >>> props.action_add
    True

Occasions metadata::

    >>> md = occasions.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'occasions_label'

    >>> md.description
    u'occasions_description'

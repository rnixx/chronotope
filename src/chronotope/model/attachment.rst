chronotope.model.attachment
===========================

Attachments
-----------

Attachments node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> attachments = chronotope['attachments']
    >>> attachments
    <Attachments object 'attachments' at ...>

    >>> attachments.__parent__
    <Chronotope object 'chronotope' at ...>

Attachments props::

    >>> props = attachments.properties
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

Attachments metadata::

    >>> md = attachments.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'attachments_label'

    >>> md.description
    u'attachments_description'

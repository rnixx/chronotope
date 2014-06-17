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

``__setitem__`` is not implemented::

    >>> attachments['1'] = object()
    Traceback (most recent call last):
      ...
    NotImplementedError: ``__setitem__`` is not implemented.

Instead attachments are created using SQLAlchemy API directly::

    >>> import uuid
    >>> import datetime
    >>> from chronotope.sql import get_session
    >>> from chronotope.model import AttachmentRecord

Get session::

    >>> session = get_session(layer.new_request())
    >>> session
    <sqlalchemy.orm.session.Session object at ...>

Create attachment record::

    >>> attachment = AttachmentRecord()
    >>> attachment.uid = str(uuid.uuid4())
    >>> attachment.creator = 'manager'
    >>> attachment.created = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment.modified = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment.title = 'Some attachment'
    >>> attachment.attachment_type = 'text'
    >>> attachment.payload = 'Some Text'

Add attachment record to database::

    >>> session.add(attachment)
    >>> session.commit()

    >>> attachment_records = session.query(AttachmentRecord).all()
    >>> attachment_records
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> attachment_records[0].id
    1

Get attachment node from attachments node::

    >>> attachment_node = attachments['1']
    >>> attachment_node
    <Attachment object '1' at ...>

Check attachment node attrs::

    >>> attachment_node.attrs['id']
    1

    >>> attachment_node.attrs['uid']
    u'...'

    >>> attachment_node.attrs['creator']
    u'manager'

    >>> attachment_node.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> attachment_node.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> attachment_node.attrs['title']
    u'Some attachment'

    >>> attachment_node.attrs['attachment_type']
    u'text'

    >>> attachment_node.attrs['payload']
    'Some Text'

    >>> attachment_node.attrs['location']
    []

    >>> attachment_node.attrs['facility']
    []

Access inexisting attachment node::

    >>> attachments['2']
    Traceback (most recent call last):
      ...
    KeyError: '2'

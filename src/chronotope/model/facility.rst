chronotope.model.facility
=========================

Facilities node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> chronotope = root['chronotope']
    >>> facilities = chronotope['facilities']
    >>> facilities
    <Facilities object 'facilities' at ...>

    >>> facilities.__parent__
    <Chronotope object 'chronotope' at ...>

Facilities props::

    >>> props = facilities.properties
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

Facilities metadata::

    >>> md = facilities.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'facilities_label'

    >>> md.description
    u'facilities_description'

Create and add Facility Node::

    >>> import datetime
    >>> from chronotope.model import Facility

    >>> facility = Facility()
    >>> facility.attrs['creator'] = u'manager'
    >>> facility.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility.attrs['title'] = u'Some facility'
    >>> facility.attrs['description'] = u'Facility description'
    >>> facility.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123'] = facility

Commit::

    >>> facilities()

Facility keys::

    >>> facilities.keys()
    ['1fbc0e0a-94bb-4726-bccb-5d1e17041123']

Facility node from facilities node::

    >>> facility = facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    >>> facility
    <Facility object '1fbc0e0a-94bb-4726-bccb-5d1e17041123' at ...>

Facility node attributes::

    >>> facility.__name__
    '1fbc0e0a-94bb-4726-bccb-5d1e17041123'

    >>> facility.attrs['uid']
    UUID('1fbc0e0a-94bb-4726-bccb-5d1e17041123')

    >>> facility.attrs['creator']
    u'manager'

    >>> facility.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> facility.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> facility.attrs['title']
    u'Some facility'

    >>> facility.attrs['description']
    u'Facility description'

    >>> facility.attrs['exists_from']
    datetime.datetime(2010, 1, 1, 0, 0)

    >>> facility.attrs['exists_to']
    datetime.datetime(2012, 1, 1, 0, 0)

    >>> facility.attrs['category']
    []

    >>> facility.attrs['location']
    []

Facility props::

    >>> props = facility.properties
    >>> props
    <cone.app.model.Properties object at ...>

    >>> props.action_up
    True

    >>> props.action_view
    True

    >>> props.action_delete
    True

    >>> props.action_up_tile
    'listing'

Facility metadata::

    >>> md = facility.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'facility_label'

    >>> md.description
    u'facility_description'

Delete facility record::

    >>> del facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    >>> facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    Traceback (most recent call last):
      ...
    KeyError: '1fbc0e0a-94bb-4726-bccb-5d1e17041123'

    >>> facilities.keys()
    []

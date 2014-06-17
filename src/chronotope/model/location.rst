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

Create and add Location Node::

    >>> import datetime
    >>> from chronotope.model import Location

    >>> location = Location()
    >>> location.attrs['creator'] = u'manager'
    >>> location.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location.attrs['lat'] = 11.37879
    >>> location.attrs['lon'] = 47.2854551
    >>> location.attrs['street'] = u'Museumstrasse'
    >>> location.attrs['zip'] = u'6020'
    >>> location.attrs['city'] = u'Innsbruck'
    >>> location.attrs['country'] = 'Austria'
    >>> locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae'] = location

Commit::

    >>> locations()

Location keys::

    >>> locations.keys()
    ['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']

Location node from locations node::

    >>> location = locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']
    >>> location
    <Location object 'd7d712ba-7f4c-4eaf-9723-8923e9d9a9ae' at ...>

Location node attributes::

    >>> location.__name__
    'd7d712ba-7f4c-4eaf-9723-8923e9d9a9ae'

    >>> location.attrs['uid']
    UUID('d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae')

    >>> location.attrs['creator']
    u'manager'

    >>> location.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> location.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> location.attrs['lat']
    11.37879

    >>> location.attrs['lon']
    47.2854551

    >>> location.attrs['street']
    u'Museumstrasse'

    >>> location.attrs['zip']
    u'6020'

    >>> location.attrs['city']
    u'Innsbruck'

    >>> location.attrs['country']
    u'Austria'

Location props::

    >>> props = location.properties
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

Location metadata::

    >>> md = location.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'location_label'

    >>> md.description
    u'location_description'

Delete location record::

    >>> del locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']
    >>> locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']
    Traceback (most recent call last):
      ...
    KeyError: 'd7d712ba-7f4c-4eaf-9723-8923e9d9a9ae'

    >>> locations.keys()
    []

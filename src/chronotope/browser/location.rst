Location tiles
==============

Imports::

    >>> from cone.tile import render_tile
    >>> from cone.app import get_root

Get model::

    >>> root = get_root()
    >>> locations = root['locations']

Check empty::

    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

Login::

    >>> layer.login('manager')

Empty add form::

    >>> request = layer.new_request()
    >>> request.params = {
    ...     'factory': 'location',
    ... }

    >>> res = render_tile(locations, request, 'add', catch_errors=False)
    >>> res.find('action="http://example.com/locations/add"') > -1
    True

Submit add form::

    >>> request.params = {
    ...     'factory': 'location',
    ...     'locationform.coordinates.lat': '11.1',
    ...     'locationform.coordinates.lon': '47.5',
    ...     'locationform.coordinates.zoom': '11',
    ...     'locationform.street': u'Museumstrasse 1',
    ...     'locationform.zip': '6020',
    ...     'locationform.city': 'Innsbruck',
    ...     'locationform.country': 'Austria',
    ...     'action.locationform.save': '1',
    ... }

    >>> res = render_tile(locations, request, 'add', catch_errors=False)

Location has been added::

    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations
      <class 'chronotope.model.location.Location'>: ...

Check location attributes::

    >>> location = locations.values()[0]
    >>> sorted(location.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('city', u'Innsbruck'), 
    ('country', u'Austria'), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('facility', []), 
    ('lat', 11.1), 
    ('lon', 47.5), 
    ('modified', datetime.datetime(...)), 
    ('state', u'draft'), 
    ('street', u'Museumstrasse 1'), 
    ('uid', UUID('...')), 
    ('zip', u'6020')]

Edit location::

    >>> request.params = {
    ...     'factory': 'location',
    ...     'locationform.coordinates.lat': '15.1',
    ...     'locationform.coordinates.lon': '42.5',
    ...     'locationform.coordinates.zoom': '16',
    ...     'locationform.street': u'Musterstrasse 1',
    ...     'locationform.zip': '1234',
    ...     'locationform.city': 'Musterort',
    ...     'locationform.country': 'Fantasia',
    ...     'action.locationform.save': '1',
    ... }
    >>> res = render_tile(location, request, 'edit', catch_errors=False)

Check whether location attributes have changed::

    >>> sorted(location.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('city', u'Musterort'), 
    ('country', u'Fantasia'), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('facility', []), 
    ('lat', 15.1), 
    ('lon', 42.5), 
    ('modified', datetime.datetime(...)), 
    ('state', u'draft'), 
    ('street', u'Musterstrasse 1'), 
    ('uid', UUID('...')), 
    ('zip', u'1234')]

Logout::

    >>> layer.logout()

Cleanup::

    >>> del locations[location.name]
    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

Location tiles
==============

Imports::

    >>> from cone.tile import render_tile
    >>> from cone.app import get_root

Get model::

    >>> root = get_root()
    >>> locations = root['locations']

Locations are empty::

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
    ...     'locationform.lat': '11.1',
    ...     'locationform.lon': '47.5',
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
    >>> location.attrs.items()
    [('uid', UUID('...')), 
    ('creator', u'manager'), 
    ('created', datetime.datetime(...)), 
    ('modified', datetime.datetime(...)), 
    ('lat', 11.1), 
    ('lon', 47.5), 
    ('street', u'Museumstrasse 1'), 
    ('zip', u'6020'), 
    ('city', u'Innsbruck'), 
    ('country', u'Austria')]

Edit location::

    >>> request.params = {
    ...     'factory': 'location',
    ...     'locationform.lat': '15.1',
    ...     'locationform.lon': '42.5',
    ...     'locationform.street': u'Musterstrasse 1',
    ...     'locationform.zip': '1234',
    ...     'locationform.city': 'Musterort',
    ...     'locationform.country': 'Fantasia',
    ...     'action.locationform.save': '1',
    ... }
    >>> res = render_tile(location, request, 'edit', catch_errors=False)

Check whether location attributes has changed::

    >>> location.attrs.items()
    [('uid', UUID('...')), 
    ('creator', u'manager'), 
    ('created', datetime.datetime(...)), 
    ('modified', datetime.datetime(...)), 
    ('lat', 15.1), 
    ('lon', 42.5), 
    ('street', u'Musterstrasse 1'), 
    ('zip', u'1234'), 
    ('city', u'Musterort'), 
    ('country', u'Fantasia')]

Logout::

    >>> layer.logout()

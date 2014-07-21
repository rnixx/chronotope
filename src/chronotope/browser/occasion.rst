chronotope.browser.occasion
===========================

Imports::

    >>> from cone.tile import render_tile
    >>> from cone.app import get_root

Get model::

    >>> root = get_root()
    >>> facilities = root['facilities']
    >>> occasions = root['occasions']

Check empty::

    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

    >>> occasions.printtree()
    <class 'chronotope.model.occasion.Occasions'>: occasions

Create dummy content::

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

    >>> facilities()

Login::

    >>> layer.login('manager')

Empty add form::

    >>> request = layer.new_request()
    >>> request.params = {
    ...     'factory': 'occasion',
    ... }

    >>> res = render_tile(occasions, request, 'add', catch_errors=False)
    >>> res.find('action="http://example.com/occasions/add"') > -1
    True

Submit add form::

    >>> request.params = {
    ...     'factory': 'occasion',
    ...     'occasionform.title': u'Some Occasion',
    ...     'occasionform.description': u'Some occasion description',
    ...     'occasionform.duration_from': '1.1.2014',
    ...     'occasionform.duration_to': '1.2.2014',
    ...     'occasionform.facility': str(facility.name),
    ...     'action.occasionform.save': '1',
    ... }
    >>> res = render_tile(occasions, request, 'add', catch_errors=False)

Occasion has been added::

    >>> occasions.printtree()
    <class 'chronotope.model.occasion.Occasions'>: occasions
      <class 'chronotope.model.occasion.Occasion'>: ...

Check occasion attributes::

    >>> occasion = occasions.values()[0]
    >>> sorted(occasion.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('description', u'Some occasion description'), 
    ('duration_from', datetime.datetime(2014, 1, 1, 0, 0)), 
    ('duration_to', datetime.datetime(2014, 2, 1, 0, 0)), 
    ('facility', [<chronotope.model.facility.FacilityRecord object at ...>]), 
    ('modified', datetime.datetime(...)), 
    ('state', u'draft'), 
    ('submitter', None), 
    ('title', u'Some Occasion'), 
    ('uid', UUID('...'))]

Edit occasion::

    >>> request.params = {
    ...     'factory': 'occasion',
    ...     'occasionform.title': u'Some Occasion changed',
    ...     'occasionform.description': u'Some occasion description changed',
    ...     'occasionform.duration_from': '1.1.2014',
    ...     'occasionform.duration_to': '1.2.2014',
    ...     'occasionform.facility': '',
    ...     'action.occasionform.save': '1',
    ... }
    >>> res = render_tile(occasion, request, 'edit', catch_errors=False)

Check whether occasion attributes have changed::

    >>> sorted(occasion.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('description', u'Some occasion description changed'), 
    ('duration_from', datetime.datetime(2014, 1, 1, 0, 0)), 
    ('duration_to', datetime.datetime(2014, 2, 1, 0, 0)), 
    ('facility', []), 
    ('modified', datetime.datetime(...)), 
    ('state', u'draft'), 
    ('submitter', None), 
    ('title', u'Some Occasion changed'), 
    ('uid', UUID('...'))]

Json view::

    >>> from chronotope.browser.occasion import json_occasion
    >>> model = root
    >>> request = layer.new_request()
    >>> request.params['q'] = 'Occ'
    >>> json_occasion(model, request)
    [{'text': u'Some Occasion changed', 
    'id': '...'}]

    >>> request.params['q'] = 'Inexistent'
    >>> json_occasion(model, request)
    []

Logout::

    >>> layer.logout()

Cleanup::

    >>> del facilities[str(facility.name)]
    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

    >>> del occasions[str(occasion.name)]
    >>> occasions.printtree()
    <class 'chronotope.model.occasion.Occasions'>: occasions

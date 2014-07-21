chronotope.browser.facility
===========================

Imports::

    >>> from cone.tile import render_tile
    >>> from cone.app import get_root

Get model::

    >>> root = get_root()
    >>> locations = root['locations']
    >>> facilities = root['facilities']

Check empty::

    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

Create dummy content::

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

    >>> locations()

    >>> request = layer.new_request()

    >>> from chronotope.model.category import add_category
    >>> cat_1 = add_category(request, 'Cat 1')

    >>> from chronotope.sql import get_session
    >>> session = get_session(request)
    >>> session.commit()

Login::

    >>> layer.login('manager')

Empty add form::

    >>> request = layer.new_request()
    >>> request.params = {
    ...     'factory': 'facility',
    ... }

    >>> res = render_tile(facilities, request, 'add', catch_errors=False)
    >>> res.find('action="http://example.com/facilities/add"') > -1
    True

Submit add form::

    >>> request.params = {
    ...     'factory': 'facility',
    ...     'facilityform.title': u'Some Facility',
    ...     'facilityform.description': u'Some facility description',
    ...     'facilityform.exists_from': '1.1.2014',
    ...     'facilityform.exists_to': '1.2.2014',
    ...     'facilityform.category': str(cat_1.uid),
    ...     'facilityform.location': str(location.name),
    ...     'action.facilityform.save': '1',
    ... }
    >>> res = render_tile(facilities, request, 'add', catch_errors=False)

Facility has been added::

    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities
     <class 'chronotope.model.facility.Facility'>: ...

Check facility attributes::

    >>> facility = facilities.values()[0]
    >>> sorted(facility.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('category', [<chronotope.model.category.CategoryRecord object at ...>]), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('description', u'Some facility description'), 
    ('exists_from', datetime.datetime(2014, 1, 1, 0, 0)), 
    ('exists_to', datetime.datetime(2014, 2, 1, 0, 0)), 
    ('location', [<chronotope.model.location.LocationRecord object at ...>]), 
    ('modified', datetime.datetime(...)), 
    ('occasion', []), 
    ('state', u'draft'), 
    ('submitter', None), 
    ('title', u'Some Facility'), 
    ('uid', UUID('...'))]

Edit facility::

    >>> request.params = {
    ...     'factory': 'facility',
    ...     'facilityform.title': u'Some Facility changed',
    ...     'facilityform.description': u'Some facility description changed',
    ...     'facilityform.exists_from': '1.1.2014',
    ...     'facilityform.exists_to': '1.2.2014',
    ...     'facilityform.category': '',
    ...     'facilityform.location': '',
    ...     'action.facilityform.save': '1',
    ... }
    >>> res = render_tile(facility, request, 'edit', catch_errors=False)

Check whether facility attributes have changed::

    >>> sorted(facility.attrs.items(), key=lambda x: x[0])
    [('attachment', []), 
    ('category', []), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('description', u'Some facility description changed'), 
    ('exists_from', datetime.datetime(2014, 1, 1, 0, 0)), 
    ('exists_to', datetime.datetime(2014, 2, 1, 0, 0)), 
    ('location', []), 
    ('modified', datetime.datetime(...)), 
    ('occasion', []), 
    ('state', u'draft'), 
    ('submitter', None), 
    ('title', u'Some Facility changed'), 
    ('uid', UUID('...'))]

Check adding new category::

    >>> request.params = {
    ...     'factory': 'facility',
    ...     'facilityform.title': u'Some Facility changed',
    ...     'facilityform.description': u'Some facility description changed',
    ...     'facilityform.exists_from': '1.1.2014',
    ...     'facilityform.exists_to': '1.2.2014',
    ...     'facilityform.category': 'New Category',
    ...     'facilityform.location': '',
    ...     'action.facilityform.save': '1',
    ... }
    >>> res = render_tile(facility, request, 'edit', catch_errors=False)
    >>> facility.attrs['category']
    [<chronotope.model.category.CategoryRecord object at ...>]

    >>> facility.attrs['category'][0].name
    u'New Category'

Check removing no longer used category::

    >>> request.params = {
    ...     'factory': 'facility',
    ...     'facilityform.title': u'Some Facility changed',
    ...     'facilityform.description': u'Some facility description changed',
    ...     'facilityform.exists_from': '1.1.2014',
    ...     'facilityform.exists_to': '1.2.2014',
    ...     'facilityform.category': '',
    ...     'facilityform.location': '',
    ...     'action.facilityform.save': '1',
    ... }
    >>> res = render_tile(facility, request, 'edit', catch_errors=False)
    >>> facility.attrs['category']
    []

    >>> from chronotope.model import CategoryRecord
    >>> session.query(CategoryRecord).all()
    []

Json view::

    >>> from chronotope.browser.facility import json_facility
    >>> model = root
    >>> request = layer.new_request()
    >>> request.params['q'] = 'Fac'
    >>> json_facility(model, request)
    [{'text': u'Some Facility changed', 
    'id': '...'}]

    >>> request.params['q'] = 'Inexistent'
    >>> json_facility(model, request)
    []

Logout::

    >>> layer.logout()

Cleanup::

    >>> del locations[str(location.name)]
    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

    >>> del facilities[str(facility.name)]
    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

Attachment tiles
================

Imports::

    >>> from cone.tile import render_tile
    >>> from cone.app import get_root

Get model::

    >>> root = get_root()
    >>> locations = root['locations']
    >>> facilities = root['facilities']
    >>> occasions = root['occasions']
    >>> attachments = root['attachments']

Check empty::

    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

    >>> occasions.printtree()
    <class 'chronotope.model.occasion.Occasions'>: occasions

    >>> attachments.printtree()
    <class 'chronotope.model.attachment.Attachments'>: attachments

Create dummy content::

    >>> import datetime
    >>> from chronotope.model import Location
    >>> from chronotope.model import Facility
    >>> from chronotope.model import Occasion

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

    >>> facility = Facility()
    >>> facility.attrs['creator'] = u'manager'
    >>> facility.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility.attrs['title'] = u'Some facility'
    >>> facility.attrs['description'] = u'Facility description'
    >>> facility.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123'] = facility

    >>> occasion = Occasion()
    >>> occasion.attrs['creator'] = u'manager'
    >>> occasion.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion.attrs['title'] = u'Some occasion'
    >>> occasion.attrs['description'] = u'Occasion description'
    >>> occasion.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasions['279af149-297d-4573-bb60-e565a8fb7a23'] = occasion

Login::

    >>> layer.login('manager')

Empty add form::

    >>> request = layer.new_request()
    >>> request.params = {
    ...     'factory': 'attachment',
    ... }

    >>> res = render_tile(attachments, request, 'add', catch_errors=False)
    >>> res.find('action="http://example.com/attachments/add"') > -1
    True

Submit add form::

    >>> request.params = {
    ...     'factory': 'attachment',
    ...     'attachmentform.title': u'Some Attachment',
    ...     'attachmentform.type': u'text',
    ...     'attachmentform.text': u'Some Attachment Text',
    ...     'attachmentform.location': str(location.name),
    ...     'attachmentform.facility': str(facility.name),
    ...     'attachmentform.occasion': str(occasion.name),
    ...     'action.attachmentform.save': '1',
    ... }
    >>> res = render_tile(attachments, request, 'add', catch_errors=False)

Facility has been added::

    >>> attachments.printtree()
    <class 'chronotope.model.attachment.Attachments'>: attachments
      <class 'chronotope.model.attachment.Attachment'>: ...

Check attachment attributes::

    >>> attachment = attachments.values()[0]
    >>> sorted(attachment.attrs.items(), key=lambda x: x[0])
    [('attachment_type', u'text'), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('facility', [<chronotope.model.facility.FacilityRecord object at ...>]), 
    ('location', [<chronotope.model.location.LocationRecord object at ...>]), 
    ('modified', datetime.datetime(...)), 
    ('occasion', [<chronotope.model.occasion.OccasionRecord object at ...>]), 
    ('payload', 'Some Attachment Text'), 
    ('state', u'draft'), 
    ('title', u'Some Attachment'), 
    ('uid', UUID('...'))]

Edit attachment::

    >>> request.params = {
    ...     'factory': 'attachment',
    ...     'attachmentform.title': u'Some Attachment changed',
    ...     'attachmentform.type': u'text',
    ...     'attachmentform.text': u'Some Attachment Text changed',
    ...     'attachmentform.location': '',
    ...     'attachmentform.facility': '',
    ...     'attachmentform.occasion': '',
    ...     'action.attachmentform.save': '1',
    ... }
    >>> res = render_tile(attachment, request, 'edit', catch_errors=False)

Check whether attachment attributes have changed::

    >>> sorted(attachment.attrs.items(), key=lambda x: x[0])
    [('attachment_type', u'text'), 
    ('created', datetime.datetime(...)), 
    ('creator', u'manager'), 
    ('facility', []), 
    ('location', []), 
    ('modified', datetime.datetime(...)), 
    ('occasion', []), 
    ('payload', 'Some Attachment Text changed'), 
    ('state', u'draft'), 
    ('title', u'Some Attachment changed'), 
    ('uid', UUID('...'))]

Logout::

    >>> layer.logout()

Cleanup::

    >>> del locations[str(location.name)]
    >>> locations.printtree()
    <class 'chronotope.model.location.Locations'>: locations

    >>> del facilities[str(facility.name)]
    >>> facilities.printtree()
    <class 'chronotope.model.facility.Facilities'>: facilities

    >>> del occasions[str(occasion.name)]
    >>> occasions.printtree()
    <class 'chronotope.model.occasion.Occasions'>: occasions

    >>> del attachments[str(attachment.name)]
    >>> attachments.printtree()
    <class 'chronotope.model.attachment.Attachments'>: attachments

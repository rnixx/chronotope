# -*- coding: utf-8 -*-

Searching
=========

Imports::

    >>> import uuid
    >>> import datetime
    >>> from cone.app import get_root
    >>> from chronotope.sql import get_session
    >>> from chronotope.model import CategoryRecord
    >>> from chronotope.model import Location
    >>> from chronotope.model import Facility
    >>> from chronotope.model import Occasion
    >>> from chronotope.model import Attachment
    >>> from chronotope.search import fulltext_search

Dummy content creation::

    >>> root = get_root()
    >>> request = layer.new_request()
    >>> session = get_session(request)

locations::

    >>> root = get_root()

    >>> locations = root['locations']

    >>> location1 = Location()
    >>> location1.attrs['creator'] = u'manager'
    >>> location1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location1.attrs['lat'] = 11.37879
    >>> location1.attrs['lon'] = 47.2854551
    >>> location1.attrs['street'] = u'Museumstrasse 1'
    >>> location1.attrs['zip'] = u'6020'
    >>> location1.attrs['city'] = u'Innsbruck'
    >>> location1.attrs['country'] = 'Austria'
    >>> locations['b8f6464b-3f62-45ab-b52a-b7906b2d74da'] = location1

    >>> location2 = Location()
    >>> location2.attrs['creator'] = u'manager'
    >>> location2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> location2.attrs['lat'] = 11.37879
    >>> location2.attrs['lon'] = 47.2854551
    >>> location2.attrs['street'] = u'Anichstrasse 1'
    >>> location2.attrs['zip'] = u'6020'
    >>> location2.attrs['city'] = u'Innsbruck'
    >>> location2.attrs['country'] = 'Austria'
    >>> locations['4252cd8d-ef3e-4b2d-8910-d6bca0b3fab6'] = location2

facilities::

    >>> facilities = root['facilities']

    >>> facility1 = Facility()
    >>> facility1.attrs['creator'] = u'manager'
    >>> facility1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility1.attrs['title'] = u'Some facility'
    >>> facility1.attrs['description'] = u'Facility description'
    >>> facility1.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility1.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facilities['8a85304c-3f16-44c2-bea1-a774670534d6'] = facility1

    >>> facility2 = Facility()
    >>> facility2.attrs['creator'] = u'manager'
    >>> facility2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility2.attrs['title'] = u'Other facility'
    >>> facility2.attrs['description'] = u'Other Facility description'
    >>> facility2.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility2.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facilities['a23d5cae-0ec5-40fd-969c-02e08f6d2dd7'] = facility2

occasions::

    >>> occasions = root['occasions']

    >>> occasion1 = Occasion()
    >>> occasion1.attrs['creator'] = u'manager'
    >>> occasion1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion1.attrs['title'] = u'Some occasion'
    >>> occasion1.attrs['description'] = u'Occasion description'
    >>> occasion1.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion1.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasions['104f3451-8895-47a2-918d-6c420394aaec'] = occasion1

    >>> occasion2 = Occasion()
    >>> occasion2.attrs['creator'] = u'manager'
    >>> occasion2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion2.attrs['title'] = u'Other occasion'
    >>> occasion2.attrs['description'] = u'Other occasion description'
    >>> occasion2.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion2.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasions['7cb5828f-2821-424f-a734-88a8ec07d266'] = occasion2

attachments::

    >>> attachments = root['attachments']

    >>> attachment1 = Attachment()
    >>> attachment1.attrs['creator'] = u'manager'
    >>> attachment1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment1.attrs['title'] = u'Some attachment'
    >>> attachment1.attrs['attachment_type'] = u'text'
    >>> attachment1.attrs['payload'] = 'Some Text'
    >>> attachments['cd6fabd0-5d4f-4e3b-a053-0315d147a0b7'] = attachment1

    >>> attachment2 = Attachment()
    >>> attachment2.attrs['creator'] = u'manager'
    >>> attachment2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment2.attrs['title'] = u'Other attachment'
    >>> attachment2.attrs['attachment_type'] = u'text'
    >>> attachment2.attrs['payload'] = 'Other Text'
    >>> attachments['7e964f01-56b9-40c8-a2f0-ac6aa53fa0e6'] = attachment2

    >>> session.commit()

No published objects, empty result::

    >>> fulltext_search(request, 'Innsbruck', 100)
    []

Authenticated user gets result::

    >>> layer.login('viewer')

    >>> fulltext_search(request, 'Innsbruck', 100)
    [<chronotope.model.location.LocationRecord object at ...>,
    <chronotope.model.location.LocationRecord object at ...>]

    >>> fulltext_search(request, 'Anichst*', 100)
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> layer.logout()

Anonymous users get published entries::

    >>> location1.state = u'published'
    >>> session.commit()

    >>> fulltext_search(request, 'Innsbruck', 100)
    [<chronotope.model.location.LocationRecord object at ...>]

Different searches::

    >>> layer.login('viewer')

    >>> fulltext_search(request, 'facility', 100)
    [<chronotope.model.facility.FacilityRecord object at ...>, 
    <chronotope.model.facility.FacilityRecord object at ...>]

    >>> fulltext_search(request, 'other facility', 100)
    [<chronotope.model.facility.FacilityRecord object at ...>]

    >>> fulltext_search(request, 'description', 100)
    [<chronotope.model...Record object at ...>, 
    <chronotope.model...Record object at ...>, 
    <chronotope.model...Record object at ...>, 
    <chronotope.model...Record object at ...>]

    >>> fulltext_search(request, 'attachment', 100)
    [<chronotope.model.attachment.AttachmentRecord object at ...>, 
    <chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> attachment2.attrs['title'] = u'Other'
    >>> session.commit()

    >>> fulltext_search(request, 'attachment', 100)
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> fulltext_search(request, 'other', 100)
    [<chronotope.model...Record object at ...>, 
    <chronotope.model...Record object at ...>, 
    <chronotope.model...Record object at ...>]

    >>> layer.logout()

Cleanup::

    >>> del locations['b8f6464b-3f62-45ab-b52a-b7906b2d74da']
    >>> del locations['4252cd8d-ef3e-4b2d-8910-d6bca0b3fab6']
    >>> del facilities['8a85304c-3f16-44c2-bea1-a774670534d6']
    >>> del facilities['a23d5cae-0ec5-40fd-969c-02e08f6d2dd7']
    >>> del occasions['104f3451-8895-47a2-918d-6c420394aaec']
    >>> del occasions['7cb5828f-2821-424f-a734-88a8ec07d266']
    >>> del attachments['cd6fabd0-5d4f-4e3b-a053-0315d147a0b7']
    >>> del attachments['7e964f01-56b9-40c8-a2f0-ac6aa53fa0e6']
    >>> session.commit()

    >>> fulltext_search(request, 'description', 100)
    []

    >>> root.printtree()
    <class 'cone.app.model.AppRoot'>: None
      <class 'cone.app.model.AppSettings'>: settings
        <class 'chronotope.model.settings.Settings'>: chronotope
      <class 'chronotope.model.about.About'>: about
        <class 'chronotope.model.about.AboutProject'>: project
        <class 'chronotope.model.about.AboutMap'>: map
        <class 'chronotope.model.about.AboutTermsOfUse'>: terms_of_use
        <class 'chronotope.model.about.AboutPrivacyPolicy'>: privacy_policy
        <class 'chronotope.model.about.AboutImprint'>: imprint
      <class 'chronotope.model.location.Locations'>: locations
      <class 'chronotope.model.facility.Facilities'>: facilities
      <class 'chronotope.model.occasion.Occasions'>: occasions
      <class 'chronotope.model.attachment.Attachments'>: attachments

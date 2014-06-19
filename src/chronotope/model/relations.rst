Model relations
===============

Imports::

    >>> import uuid
    >>> import datetime
    >>> from cone.app import get_root
    >>> from chronotope.sql import get_session
    >>> from chronotope.model import (
    ...     CategoryRecord,
    ...     Location,
    ...     Facility,
    ...     Occasion,
    ...     Attachment,
    ... )

Fetch containers::

    >>> root = get_root()
    >>> chronotope = root['chronotope']

Create categories::

    >>> request = layer.new_request()
    >>> session = get_session(request)

    >>> category1 = CategoryRecord()
    >>> category1.uid = uuid.UUID('3d9f44e1-00cb-42d4-82a3-f32f06e09e4f')
    >>> category1.name = 'Category 1'
    >>> session.add(category1)

    >>> category2 = CategoryRecord()
    >>> category2.uid = uuid.UUID('16a83305-2b60-4f29-b225-3c64a1f0f120')
    >>> category2.name = 'Category 2'
    >>> session.add(category2)

Create locations::

    >>> locations = chronotope['locations']

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

Create facilities::

    >>> facilities = chronotope['facilities']

    >>> facility1 = Facility()
    >>> facility1.attrs['creator'] = u'manager'
    >>> facility1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility1.attrs['title'] = u'Some facility'
    >>> facility1.attrs['description'] = u'Facility description'
    >>> facility1.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility1.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facility1.attrs['category'].append(category1)
    >>> facility1.attrs['category'].append(category2)
    >>> facility1.attrs['location'].append(location1.record)
    >>> facilities['8a85304c-3f16-44c2-bea1-a774670534d6'] = facility1

    >>> facility2 = Facility()
    >>> facility2.attrs['creator'] = u'manager'
    >>> facility2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> facility2.attrs['title'] = u'Other facility'
    >>> facility2.attrs['description'] = u'Other Facility description'
    >>> facility2.attrs['exists_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> facility2.attrs['exists_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> facility2.attrs['category'].append(category1)
    >>> facility2.attrs['location'].append(location1.record)
    >>> facility2.attrs['location'].append(location2.record)
    >>> facilities['a23d5cae-0ec5-40fd-969c-02e08f6d2dd7'] = facility2

Check references and back references of facility to location reference::

    >>> facility1.record.location
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> facility2.record.location
    [<chronotope.model.location.LocationRecord object at ...>, 
    <chronotope.model.location.LocationRecord object at ...>]

    >>> location1.record.facility
    [<chronotope.model.facility.FacilityRecord object at ...>, 
    <chronotope.model.facility.FacilityRecord object at ...>]

    >>> location2.record.facility
    [<chronotope.model.facility.FacilityRecord object at ...>]

Check references and back references of facility to category reference::

    >>> facility1.record.category
    [<chronotope.model.category.CategoryRecord object at ...>, 
    <chronotope.model.category.CategoryRecord object at ...>]

    >>> facility2.record.category
    [<chronotope.model.category.CategoryRecord object at ...>]

    >>> category1.facility
    [<chronotope.model.facility.FacilityRecord object at ...>, 
    <chronotope.model.facility.FacilityRecord object at ...>]

    >>> category2.facility
    [<chronotope.model.facility.FacilityRecord object at ...>]

Create occasions::

    >>> occasions = chronotope['occasions']

    >>> occasion1 = Occasion()
    >>> occasion1.attrs['creator'] = u'manager'
    >>> occasion1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion1.attrs['title'] = u'Some occasion'
    >>> occasion1.attrs['description'] = u'Occasion description'
    >>> occasion1.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion1.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasion1.attrs['facility'].append(facility1.record)
    >>> occasions['104f3451-8895-47a2-918d-6c420394aaec'] = occasion1

    >>> occasion2 = Occasion()
    >>> occasion2.attrs['creator'] = u'manager'
    >>> occasion2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion2.attrs['title'] = u'Other occasion'
    >>> occasion2.attrs['description'] = u'Other occasion description'
    >>> occasion2.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion2.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasion2.attrs['facility'].append(facility1.record)
    >>> occasion2.attrs['facility'].append(facility2.record)
    >>> occasions['7cb5828f-2821-424f-a734-88a8ec07d266'] = occasion2

Check references and back references of occasion to facility reference::

    >>> occasion1.record.facility
    [<chronotope.model.facility.FacilityRecord object at ...>]

    >>> occasion2.record.facility
    [<chronotope.model.facility.FacilityRecord object at ...>, 
    <chronotope.model.facility.FacilityRecord object at ...>]

    >>> facility1.record.occasion
    [<chronotope.model.occasion.OccasionRecord object at ...>, 
    <chronotope.model.occasion.OccasionRecord object at ...>]

    >>> facility2.record.occasion
    [<chronotope.model.occasion.OccasionRecord object at ...>]

Create attachments::

    >>> attachments = chronotope['attachments']

    >>> attachment1 = Attachment()
    >>> attachment1.attrs['creator'] = u'manager'
    >>> attachment1.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment1.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment1.attrs['title'] = u'Some attachment'
    >>> attachment1.attrs['attachment_type'] = u'text'
    >>> attachment1.attrs['payload'] = 'Some Text'
    >>> attachment1.attrs['location'].append(location1.record)
    >>> attachment1.attrs['facility'].append(facility1.record)
    >>> attachment1.attrs['facility'].append(facility2.record)
    >>> attachment1.attrs['occasion'].append(occasion1.record)
    >>> attachments['cd6fabd0-5d4f-4e3b-a053-0315d147a0b7'] = attachment1

    >>> attachment2 = Attachment()
    >>> attachment2.attrs['creator'] = u'manager'
    >>> attachment2.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment2.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment2.attrs['title'] = u'Other attachment'
    >>> attachment2.attrs['attachment_type'] = u'text'
    >>> attachment2.attrs['payload'] = 'Other Text'
    >>> attachment2.attrs['location'].append(location1.record)
    >>> attachment2.attrs['location'].append(location2.record)
    >>> attachment2.attrs['facility'].append(facility1.record)
    >>> attachment2.attrs['occasion'].append(occasion2.record)
    >>> attachments['7e964f01-56b9-40c8-a2f0-ac6aa53fa0e6'] = attachment2

Check references and back references of attachment to location reference::

    >>> attachment1.record.location
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> attachment2.record.location
    [<chronotope.model.location.LocationRecord object at ...>, 
    <chronotope.model.location.LocationRecord object at ...>]

    >>> location1.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>, 
    <chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> location2.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

Check references and back references of attachment to facility reference::

    >>> attachment1.record.location
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> attachment2.record.location
    [<chronotope.model.location.LocationRecord object at ...>, 
    <chronotope.model.location.LocationRecord object at ...>]

    >>> facility1.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>, 
    <chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> facility2.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

Check references and back references of attachment to occasion reference::

    >>> attachment1.record.occasion
    [<chronotope.model.occasion.OccasionRecord object at ...>]

    >>> attachment2.record.occasion
    [<chronotope.model.occasion.OccasionRecord object at ...>]

    >>> occasion1.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

    >>> occasion2.record.attachment
    [<chronotope.model.attachment.AttachmentRecord object at ...>]

Commit::

    >>> from chronotope.sql import get_session
    >>> session = get_session(layer.current_request)
    >>> session.commit()

Cleanup::

    >>> chronotope.printtree()
    <class 'chronotope.model.Chronotope'>: chronotope
      <class 'chronotope.model.location.Locations'>: locations
        <class 'chronotope.model.location.Location'>: 4252cd8d...
        <class 'chronotope.model.location.Location'>: b8f6464b...
      <class 'chronotope.model.facility.Facilities'>: facilities
        <class 'chronotope.model.facility.Facility'>: 8a85304c...
        <class 'chronotope.model.facility.Facility'>: a23d5cae...
      <class 'chronotope.model.occasion.Occasions'>: occasions
        <class 'chronotope.model.occasion.Occasion'>: 104f345...
        <class 'chronotope.model.occasion.Occasion'>: 7cb5828f...
      <class 'chronotope.model.attachment.Attachments'>: attachments
        <class 'chronotope.model.attachment.Attachment'>: 7e964f01...
        <class 'chronotope.model.attachment.Attachment'>: cd6fabd0...

    >>> session.delete(category1)
    >>> session.delete(category2)
    >>> del locations['b8f6464b-3f62-45ab-b52a-b7906b2d74da']
    >>> del locations['4252cd8d-ef3e-4b2d-8910-d6bca0b3fab6']
    >>> del facilities['8a85304c-3f16-44c2-bea1-a774670534d6']
    >>> del facilities['a23d5cae-0ec5-40fd-969c-02e08f6d2dd7']
    >>> del occasions['104f3451-8895-47a2-918d-6c420394aaec']
    >>> del occasions['7cb5828f-2821-424f-a734-88a8ec07d266']
    >>> del attachments['cd6fabd0-5d4f-4e3b-a053-0315d147a0b7']
    >>> del attachments['7e964f01-56b9-40c8-a2f0-ac6aa53fa0e6']
    >>> session.commit()

    >>> chronotope.printtree()
    <class 'chronotope.model.Chronotope'>: chronotope
      <class 'chronotope.model.location.Locations'>: locations
      <class 'chronotope.model.facility.Facilities'>: facilities
      <class 'chronotope.model.occasion.Occasions'>: occasions
      <class 'chronotope.model.attachment.Attachments'>: attachments

Model relations
===============

Imports::

    >>> import datetime
    >>> from cone.app import get_root
    >>> from chronotope.model import (
    ...     Location,
    ...     Facility,
    ...     Occasion,
    ...     Attachment,
    ... )

Fetch containers::

    >>> root = get_root()
    >>> chronotope = root['chronotope']

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
    >>> facility2.attrs['location'].append(location1.record)
    >>> facility2.attrs['location'].append(location2.record)
    >>> facilities['a23d5cae-0ec5-40fd-969c-02e08f6d2dd7'] = facility2

Check references and back references::

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


104f3451-8895-47a2-918d-6c420394aaec
7cb5828f-2821-424f-a734-88a8ec07d266
cd6fabd0-5d4f-4e3b-a053-0315d147a0b7
7e964f01-56b9-40c8-a2f0-ac6aa53fa0e6
88eda192-1f55-4f21-949b-60c6762b5d09
2687cb6a-c1eb-4ff7-a410-19bd5836349a
e5e6eede-6a5e-4c23-9da3-a1bd2c272fd0
dcd08dce-c646-447a-9dd0-47596b51733e
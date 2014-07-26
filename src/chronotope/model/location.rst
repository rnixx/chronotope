chronotope.model.location
=========================

Locations node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> locations = root['locations']
    >>> locations
    <Locations object 'locations' at ...>

    >>> locations.__parent__
    <AppRoot object 'None' at ...>

Locations ACL::

    >>> locations.__acl__
    [('Allow', 'role:viewer', ['view']), 
    ('Allow', 'role:editor', ['view', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'add']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

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

    >>> md.creator
    >>> md.created
    >>> md.modified

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

Initial state and ACL::

    >>> location.attrs['state']
    u'draft'

    >>> location.__acl__
    [('Allow', 'role:viewer', ['view']), 
    ('Allow', 'role:editor', ['view', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'view', 'add', 'edit']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

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

    >>> props.action_edit
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
    u'Museumstrasse 6020 Innsbruck'

    >>> md.creator
    u'manager'

    >>> md.created
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> md.modified
    datetime.datetime(2014, 6, 1, 0, 0)

Location workflow state::

    >>> from repoze.workflow import get_workflow
    >>> from cone.app.interfaces import IWorkflowState

    >>> IWorkflowState.providedBy(location)
    True

    >>> workflow = get_workflow(location.__class__,
    ...                         location.properties.wf_name)
    >>> workflow
    <repoze.workflow.workflow.Workflow object at ...>

    >>> location.state
    u'draft'

    >>> layer.login('manager')
    >>> workflow.transition(location,
    ...                     layer.new_request(),
    ...                     'draft_2_published')
    >>> location()
    >>> layer.logout()

    >>> location.state
    u'published'

Search and fetch functions::

    >>> import uuid
    >>> from chronotope.model.location import (
    ...     location_by_uid,
    ...     locations_by_uid,
    ...     search_locations,
    ... )
    >>> request = layer.new_request()
    >>> location_by_uid(request, 'd7d712ba-7f4c-4eaf-9723-8923e9d9a9ae')
    <chronotope.model.location.LocationRecord object at ...>

    >>> location_by_uid(request, uuid.uuid4())

    >>> locations_by_uid(request, ['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae'])
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> locations_by_uid(request, [uuid.uuid4()])
    []

    >>> search_locations(request, 'Museum')
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> search_locations(request, '6020')
    [<chronotope.model.location.LocationRecord object at ...>]

    >>> search_locations(request, 'Inns')
    [<chronotope.model.location.LocationRecord object at ...>]

Delete location record::

    >>> del locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']
    >>> locations['d7d712ba-7f4c-4eaf-9723-8923e9d9a9ae']
    Traceback (most recent call last):
      ...
    KeyError: 'd7d712ba-7f4c-4eaf-9723-8923e9d9a9ae'

    >>> locations.keys()
    []

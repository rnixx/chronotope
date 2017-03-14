chronotope.model.facility
=========================

Facilities node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> facilities = root['facilities']
    >>> facilities
    <Facilities object 'facilities' at ...>

    >>> facilities.__parent__
    <AppRoot object 'None' at ...>

Facilities ACL::

    >>> facilities.__acl__
    [('Allow', 'system.Authenticated', ['view']), 
    ('Allow', 'role:viewer', ['view', 'list']), 
    ('Allow', 'role:editor', ['view', 'list', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'add']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

Facilities props::

    >>> props = facilities.properties
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

Facilities metadata::

    >>> md = facilities.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'facilities_label'

    >>> md.description
    u'facilities_description'

Create and add Facility Node::

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

Commit::

    >>> facilities()

Facility keys::

    >>> facilities.keys()
    ['1fbc0e0a-94bb-4726-bccb-5d1e17041123']

Facility node from facilities node::

    >>> facility = facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    >>> facility
    <Facility object '1fbc0e0a-94bb-4726-bccb-5d1e17041123' at ...>

Initial state and ACL::

    >>> facility.attrs['state']
    u'draft'

    >>> facility.__acl__
    [('Allow', 'system.Authenticated', ['view']), 
    ('Allow', 'role:viewer', ['view', 'list']), 
    ('Allow', 'role:editor', ['view', 'list', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'view', 'add', 'edit']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

Facility node attributes::

    >>> facility.__name__
    '1fbc0e0a-94bb-4726-bccb-5d1e17041123'

    >>> facility.attrs['uid']
    UUID('1fbc0e0a-94bb-4726-bccb-5d1e17041123')

    >>> facility.attrs['creator']
    u'manager'

    >>> facility.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> facility.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> facility.attrs['title']
    u'Some facility'

    >>> facility.attrs['description']
    u'Facility description'

    >>> facility.attrs['exists_from']
    datetime.datetime(2010, 1, 1, 0, 0)

    >>> facility.attrs['exists_to']
    datetime.datetime(2012, 1, 1, 0, 0)

    >>> facility.attrs['category']
    []

    >>> facility.attrs['location']
    []

Facility props::

    >>> props = facility.properties
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

Facility metadata::

    >>> md = facility.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'Some facility'

    >>> md.description
    u'Facility description'

    >>> md.creator
    u'manager'

    >>> md.created
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> md.modified
    datetime.datetime(2014, 6, 1, 0, 0)

Location workflow state::

    >>> from repoze.workflow import get_workflow
    >>> from cone.app.interfaces import IWorkflowState

    >>> IWorkflowState.providedBy(facility)
    True

    >>> workflow = get_workflow(facility.__class__,
    ...                         facility.workflow_name)
    >>> workflow
    <repoze.workflow.workflow.Workflow object at ...>

    >>> facility.state
    u'draft'

    >>> layer.login('manager')
    >>> workflow.transition(facility,
    ...                     layer.new_request(),
    ...                     'draft_2_published')
    >>> facility()
    >>> layer.logout()

    >>> facility.state
    u'published'

Search and fetch functions::

    >>> import uuid
    >>> from chronotope.model.facility import facility_by_uid
    >>> from chronotope.model.facility import facilities_by_uid
    >>> from chronotope.model.facility import search_facilities

    >>> request = layer.new_request()
    >>> facility_by_uid(request, '1fbc0e0a-94bb-4726-bccb-5d1e17041123')
    <chronotope.model.facility.FacilityRecord object at ...>

    >>> facility_by_uid(request, uuid.uuid4())

    >>> facilities_by_uid(request, ['1fbc0e0a-94bb-4726-bccb-5d1e17041123'])
    [<chronotope.model.facility.FacilityRecord object at ...>]

    >>> facilities_by_uid(request, [uuid.uuid4()])
    []

    >>> search_facilities(request, 'Faci')
    [<chronotope.model.facility.FacilityRecord object at ...>]

Delete facility record::

    >>> del facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    >>> facilities['1fbc0e0a-94bb-4726-bccb-5d1e17041123']
    Traceback (most recent call last):
      ...
    KeyError: '1fbc0e0a-94bb-4726-bccb-5d1e17041123'

    >>> facilities.keys()
    []

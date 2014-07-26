chronotope.model.attachment
===========================

Attachments node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> attachments = root['attachments']
    >>> attachments
    <Attachments object 'attachments' at ...>

    >>> attachments.__parent__
    <AppRoot object 'None' at ...>

Attachments ACL::

    >>> attachments.__acl__
    [('Allow', 'system.Authenticated', ['view']), 
    ('Allow', 'role:viewer', ['view', 'list']), 
    ('Allow', 'role:editor', ['view', 'list', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'add']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

Attachments props::

    >>> props = attachments.properties
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

Attachments metadata::

    >>> md = attachments.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'attachments_label'

    >>> md.description
    u'attachments_description'

Create and add Attachment Node::

    >>> import datetime
    >>> from chronotope.model import Attachment

    >>> attachment = Attachment()
    >>> attachment.attrs['creator'] = u'manager'
    >>> attachment.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> attachment.attrs['title'] = u'Some attachment'
    >>> attachment.attrs['attachment_type'] = u'text'
    >>> attachment.attrs['payload'] = 'Some Text'
    >>> attachments['b495eefd-bb92-4108-88c4-e04c82efe0a7'] = attachment

Commit::

    >>> attachments()

Attachment keys::

    >>> attachments.keys()
    ['b495eefd-bb92-4108-88c4-e04c82efe0a7']

Attachment node from attachments node::

    >>> attachment = attachments['b495eefd-bb92-4108-88c4-e04c82efe0a7']
    >>> attachment
    <Attachment object 'b495eefd-bb92-4108-88c4-e04c82efe0a7' at ...>

Initial state and ACL::

    >>> attachment.attrs['state']
    u'draft'

    >>> attachment.__acl__
    [('Allow', 'system.Authenticated', ['view']), 
    ('Allow', 'role:viewer', ['view', 'list']), 
    ('Allow', 'role:editor', ['view', 'list', 'add', 'edit']), 
    ('Allow', 'role:admin', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state']), 
    ('Allow', 'role:manager', ['view', 'list', 'add', 'edit', 'delete', 'cut', 
    'copy', 'paste', 'change_state', 'manage']), 
    ('Allow', 'system.Everyone', ['login', 'view', 'add', 'edit']), 
    ('Deny', 'system.Everyone', <pyramid.security.AllPermissionsList object at ...>)]

Attachment node attributes::

    >>> attachment.__name__
    'b495eefd-bb92-4108-88c4-e04c82efe0a7'

    >>> attachment.attrs['uid']
    UUID('b495eefd-bb92-4108-88c4-e04c82efe0a7')

    >>> attachment.attrs['creator']
    u'manager'

    >>> attachment.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> attachment.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> attachment.attrs['title']
    u'Some attachment'

    >>> attachment.attrs['attachment_type']
    u'text'

    >>> attachment.attrs['payload']
    'Some Text'

    >>> attachment.attrs['location']
    []

    >>> attachment.attrs['facility']
    []

    >>> attachment.attrs['occasion']
    []

Attachment props::

    >>> props = attachment.properties
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

Attachment metadata::

    >>> md = attachment.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'Some attachment'

    >>> md.creator
    u'manager'

    >>> md.created
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> md.modified
    datetime.datetime(2014, 6, 1, 0, 0)

Attachment workflow state::

    >>> from repoze.workflow import get_workflow
    >>> from cone.app.interfaces import IWorkflowState

    >>> IWorkflowState.providedBy(attachment)
    True

    >>> workflow = get_workflow(attachment.__class__,
    ...                         attachment.properties.wf_name)
    >>> workflow
    <repoze.workflow.workflow.Workflow object at ...>

    >>> attachment.state
    u'draft'

    >>> layer.login('manager')
    >>> workflow.transition(attachment,
    ...                     layer.new_request(),
    ...                     'draft_2_published')
    >>> attachment()
    >>> layer.logout()

    >>> attachment.state
    u'published'

Delete attachment record::

    >>> del attachments['b495eefd-bb92-4108-88c4-e04c82efe0a7']
    >>> attachments['b495eefd-bb92-4108-88c4-e04c82efe0a7']
    Traceback (most recent call last):
      ...
    KeyError: 'b495eefd-bb92-4108-88c4-e04c82efe0a7'

    >>> attachments.keys()
    []

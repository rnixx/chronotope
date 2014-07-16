chronotope.model.occasion
=========================

Occasions node::

    >>> from cone.app import get_root
    >>> root = get_root()
    >>> occasions = root['occasions']
    >>> occasions
    <Occasions object 'occasions' at ...>

    >>> occasions.__parent__
    <AppRoot object 'None' at ...>

Occasions props::

    >>> props = occasions.properties
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

Occasions metadata::

    >>> md = occasions.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'occasions_label'

    >>> md.description
    u'occasions_description'

Create and add Occasion Node::

    >>> import datetime
    >>> from chronotope.model import Occasion

    >>> occasion = Occasion()
    >>> occasion.attrs['creator'] = u'manager'
    >>> occasion.attrs['created'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion.attrs['modified'] = datetime.datetime(2014, 06, 01, 0, 0)
    >>> occasion.attrs['title'] = u'Some occasion'
    >>> occasion.attrs['description'] = u'Occasion description'
    >>> occasion.attrs['duration_from'] = datetime.datetime(2010, 01, 01, 0, 0)
    >>> occasion.attrs['duration_to'] = datetime.datetime(2012, 01, 01, 0, 0)
    >>> occasions['279af149-297d-4573-bb60-e565a8fb7a23'] = occasion

Commit::

    >>> occasions()

Occasion keys::

    >>> occasions.keys()
    ['279af149-297d-4573-bb60-e565a8fb7a23']

Occasion node from occasions node::

    >>> occasion = occasions['279af149-297d-4573-bb60-e565a8fb7a23']
    >>> occasion
    <Occasion object '279af149-297d-4573-bb60-e565a8fb7a23' at ...>

Occasion node attributes::

    >>> occasion.__name__
    '279af149-297d-4573-bb60-e565a8fb7a23'

    >>> occasion.attrs['uid']
    UUID('279af149-297d-4573-bb60-e565a8fb7a23')

    >>> occasion.attrs['creator']
    u'manager'

    >>> occasion.attrs['created']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> occasion.attrs['modified']
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> occasion.attrs['title']
    u'Some occasion'

    >>> occasion.attrs['description']
    u'Occasion description'

    >>> occasion.attrs['duration_from']
    datetime.datetime(2010, 1, 1, 0, 0)

    >>> occasion.attrs['duration_to']
    datetime.datetime(2012, 1, 1, 0, 0)

    >>> occasion.attrs['facility']
    []

Occasion props::

    >>> props = occasion.properties
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

Occasion metadata::

    >>> md = occasion.metadata
    >>> md
    <cone.app.model.Metadata object at ...>

    >>> md.title
    u'Some occasion'

    >>> md.description
    u'Occasion description'

    >>> md.creator
    u'manager'

    >>> md.created
    datetime.datetime(2014, 6, 1, 0, 0)

    >>> md.modified
    datetime.datetime(2014, 6, 1, 0, 0)

Occasion workflow state::

    >>> from repoze.workflow import get_workflow
    >>> from cone.app.interfaces import IWorkflowState

    >>> IWorkflowState.providedBy(occasion)
    True

    >>> workflow = get_workflow(occasion.__class__,
    ...                         occasion.properties.wf_name)
    >>> workflow
    <repoze.workflow.workflow.Workflow object at ...>

    >>> occasion.state
    u'draft'

    >>> layer.login('manager')
    >>> workflow.transition(occasion,
    ...                     layer.new_request(),
    ...                     'draft_2_published')
    >>> occasion()
    >>> layer.logout()

    >>> occasion.state
    u'published'

Search and fetch functions::

    >>> import uuid
    >>> from chronotope.model.occasion import (
    ...     occasion_by_uid,
    ...     occasions_by_uid,
    ...     search_occasions,
    ... )
    >>> request = layer.new_request()
    >>> occasion_by_uid(request, '279af149-297d-4573-bb60-e565a8fb7a23')
    <chronotope.model.occasion.OccasionRecord object at ...>

    >>> occasion_by_uid(request, uuid.uuid4())

    >>> occasions_by_uid(request, ['279af149-297d-4573-bb60-e565a8fb7a23'])
    [<chronotope.model.occasion.OccasionRecord object at ...>]

    >>> occasions_by_uid(request, [uuid.uuid4()])
    []

    >>> search_occasions(request, 'Occa')
    [<chronotope.model.occasion.OccasionRecord object at ...>]

Delete occasion record::

    >>> del occasions['279af149-297d-4573-bb60-e565a8fb7a23']
    >>> occasions['279af149-297d-4573-bb60-e565a8fb7a23']
    Traceback (most recent call last):
      ...
    KeyError: '279af149-297d-4573-bb60-e565a8fb7a23'

    >>> occasions.keys()
    []

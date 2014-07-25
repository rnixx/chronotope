from pyramid.i18n import TranslationStringFactory
from pyramid.security import (
    Everyone,
    Allow,
    Deny,
    ALL_PERMISSIONS,
)
from chronotope.security import (
    viewer_permissions,
    editor_permissions,
    admin_permissions,
    manager_permissions,
)


_ = TranslationStringFactory('chronotope')


publication_transition_names = {
    'draft_2_published': _('draft_2_published', default='Publish'),
    'draft_2_declined': _('draft_2_declined', default='Decline'),
    'published_2_draft': _('published_2_draft', default='Retract'),
    'published_2_declined': _('published_2_declined', default='Decline'),
    'declined_2_draft': _('declined_2_draft', default='Retract'),
    'declined_2_published': _('declined_2_published', default='Publish'),
}


# ACLs for publication workflow states
publication_state_acls = dict()
publication_state_acls['draft'] = [
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login', 'view', 'add', 'edit']),
    (Deny, Everyone, ALL_PERMISSIONS),
]
publication_state_acls['published'] = [
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login', 'view']),
    (Deny, Everyone, ALL_PERMISSIONS),
]
publication_state_acls['declined'] = [
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

from pyramid.i18n import TranslationStringFactory
from pyramid.security import (
    Everyone,
    Allow,
    Deny,
    ALL_PERMISSIONS,
)
from chronotope.security import (
    authenticated_permissions,
    viewer_permissions,
    editor_permissions,
    admin_permissions,
    manager_permissions,
)


_ = TranslationStringFactory('chronotope')


# ACLs for publication workflow states
publication_state_acls = dict()
publication_state_acls['draft'] = [
    (Allow, 'system.Authenticated', authenticated_permissions),
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login', 'view', 'add', 'edit']),
    (Deny, Everyone, ALL_PERMISSIONS),
]
publication_state_acls['published'] = [
    (Allow, 'system.Authenticated', authenticated_permissions),
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login', 'view']),
    (Deny, Everyone, ALL_PERMISSIONS),
]
publication_state_acls['declined'] = [
    (Allow, 'system.Authenticated', authenticated_permissions),
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

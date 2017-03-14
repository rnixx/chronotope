from chronotope.security import admin_permissions
from chronotope.security import authenticated_permissions
from chronotope.security import editor_permissions
from chronotope.security import manager_permissions
from chronotope.security import viewer_permissions
from pyramid.i18n import TranslationStringFactory
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import Everyone


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

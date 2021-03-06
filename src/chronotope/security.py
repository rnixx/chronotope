from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import Everyone


# permission sets
authenticated_permissions = [
    'view',
]
viewer_permissions = [
    'view', 'list',
]
editor_permissions = [
    'view', 'list', 'add', 'edit',
]
admin_permissions = [
    'view', 'list', 'add', 'edit', 'delete', 'cut', 'copy',
    'paste', 'change_state',
]
manager_permissions = [
    'view', 'list', 'add', 'edit', 'delete', 'cut', 'copy',
    'paste', 'change_state', 'manage',
]
root_everyone_permissions = [
    'login', 'view',
]
container_everyone_permissions = [
    'login', 'add',
]


# chronotope root ACL
chronotope_root_acl = [
    (Allow, 'system.Authenticated', authenticated_permissions),
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager',  manager_permissions),
    (Allow, Everyone, root_everyone_permissions),
    (Deny, Everyone, ALL_PERMISSIONS),
]


# chronotope about ACL
chronotope_about_acl = [
    (Allow, Everyone, ['view']),
]


# chronotope container ACL
chronotope_container_acl = [
    (Allow, 'system.Authenticated', authenticated_permissions),
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, container_everyone_permissions),
    (Deny, Everyone, ALL_PERMISSIONS),
]

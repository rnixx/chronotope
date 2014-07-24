from pyramid.security import (
    Everyone,
    Allow,
    Deny,
    ALL_PERMISSIONS,
)


# permission sets
viewer_permissions = ['view']
editor_permissions = ['view', 'add', 'edit']
admin_permissions = ['view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste',
                     'change_state']
manager_permissions = admin_permissions + ['manage']


# chronotope root ACL
chronotope_root_acl = [
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager',  manager_permissions),
    (Allow, Everyone, ['login', 'view']),
    (Deny, Everyone, ALL_PERMISSIONS),
]


# chronotope default ACL
chronotope_default_acl = [
    (Allow, 'role:viewer', viewer_permissions),
    (Allow, 'role:editor', editor_permissions),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', manager_permissions),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

from pyramid.security import (
    Everyone,
    Allow,
    Deny,
    ALL_PERMISSIONS,
)


# default chronotope ACL
admin_permissions = [
    'view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state',
]
manager_permissions = ['manage']
chronotope_default_acl = [
    (Allow, 'role:viewer', ['view']),
    (Allow, 'role:editor', ['view', 'add', 'edit']),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', admin_permissions + manager_permissions),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

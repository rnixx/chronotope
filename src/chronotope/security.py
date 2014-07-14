from pyramid.security import (
    Everyone,
    Allow,
    Deny,
    ALL_PERMISSIONS,
)


# chronotope root ACL
admin_permissions = [
    'view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state',
]
manager_permissions = ['manage']
chronotope_root_acl = [
    (Allow, 'role:viewer', ['view']),
    (Allow, 'role:editor', ['view', 'add', 'edit']),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', admin_permissions + manager_permissions),
    (Allow, Everyone, ['login', 'view']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

# chronotope content ACL
admin_permissions = [
    'view', 'add', 'edit', 'delete', 'cut', 'copy', 'paste', 'change_state',
]
manager_permissions = ['manage']
chronotope_content_acl = [
    (Allow, 'role:viewer', ['view']),
    (Allow, 'role:editor', ['view', 'add', 'edit']),
    (Allow, 'role:admin', admin_permissions),
    (Allow, 'role:manager', admin_permissions + manager_permissions),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS),
]

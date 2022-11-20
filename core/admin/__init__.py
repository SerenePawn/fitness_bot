from .commands import (
    create_admin,
    create_db
)


MANAGE_CMDS = {
    'createdb': {
        'cmd': create_db,
        'struct': '',
    },
    'createstaff': {
        'cmd': create_admin,
        'struct': '<user_id> <is_staff> <is_superadmin>',
    },
}

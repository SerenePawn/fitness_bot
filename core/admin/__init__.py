from .commands import (
    create_admin,
    init_db,
    migrate,
)


MANAGE_CMDS = {
    'initdb': {
        'cmd': init_db,
        'struct': '',
    },
    'createstaff': {
        'cmd': create_admin,
        'struct': '<user_id> <is_staff> <is_superadmin>',
    },
    'migrate': {
        'cmd': migrate,
        'struct': '<migration file>',
    },
}

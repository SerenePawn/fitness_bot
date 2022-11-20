from core.db.misc.admin_commands import (
    set_govs,
    alist
)


class AdminCmdsEnum:
    SET_GOVS = 'set_govs'
    ADMIN_LIST = 'alist'

    CMDS = {
        SET_GOVS: set_govs,
        ADMIN_LIST: alist,
    }

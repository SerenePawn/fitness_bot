from core.db.misc.admin_commands import *


class AdminCmdsEnum:
    SET_GOVS = 'set_govs'
    ADMIN_LIST = 'alist'

    CMDS = {
        SET_GOVS: set_govs,
        ADMIN_LIST: alist,
    }

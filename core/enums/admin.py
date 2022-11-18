from core.db.misc.admin_commands import *


class AdminCmdsEnum:
    CREATE_DB = 'create_db'
    SET_GOVS = 'set_govs'

    CMDS = {
        CREATE_DB: create_db,
        SET_GOVS: set_govs,
    }

from core.enums.govs import GovsTypeEnum
from core.db.core_db import DatabaseManager
from core.db.misc.exceptions import InvalidParams


async def create_db(mgr: DatabaseManager, params: list):
    """ Initialize db from sql """
    if params:
        raise InvalidParams('This func cannot have any params')
    with open('core/db/sql/create_db.sql') as f:
        await mgr.execute_many(f.read())


async def set_govs(mgr: DatabaseManager, params: list):
    """ Set governors """
    if len(params) != 3:
        raise InvalidParams('This func need params: <id> <stuff|admin> <true|false>')
    user_id, gov_type, val = params
    if gov_type not in GovsTypeEnum.CHOICES:
        raise InvalidParams('Invalid gov_type. <stuff|admin> allowed only.')
    mgr.update_data('staff', 'id = $1', **{'id': user_id, gov_type: val})

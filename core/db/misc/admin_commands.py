from core.enums.govs import GovsTypeEnum
from core.db.core_db import DatabaseManager
from core.db.misc.exceptions import InvalidParams
from core.app import State

STAFF_T = 'staff'


async def set_govs(state: State, params: list):
    """ Set governors """
    if len(params) != 3:
        raise InvalidParams(f'This func need params: <id> <{"|".join([i for i in GovsTypeEnum.CHOICES])}> <true|false>')
    user_id, gov_type, val = params
    if gov_type not in GovsTypeEnum.CHOICES:
        raise InvalidParams(f'Invalid gov_type. <{"|".join([i for i in GovsTypeEnum.CHOICES])}> allowed only.')

    await state.db.update_data(STAFF_T, {'id': user_id}, {gov_type: val})


async def alist(state: State, params: list):
    """ Admin list """
    if params:
        raise InvalidParams('This func cannot have any params')

    result = await state.db.get_data_all(STAFF_T)
    return result or "Admin list is empty."

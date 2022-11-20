from aiogram.types.user import User

from core.enums.govs import GovsTypeEnum
from core.db.core_db import DatabaseManager
from core.db.misc.exceptions import InvalidParams
from core.app import State

STAFF_T = 'staff'


async def set_govs(state: State, from_user: User, params: list):
    """ Set governors """
    if len(params) != 3:
        await state.bot.send_message(from_user.id, f'This func need params: <id> <{"|".join([i for i in GovsTypeEnum.CHOICES])}> <true|false>')
        return
    user_id, gov_type, val = params
    if gov_type not in GovsTypeEnum.CHOICES:
        await state.bot.send_message(from_user.id, f'Invalid gov_type. <{"|".join([i for i in GovsTypeEnum.CHOICES])}> allowed only.')
        return

    await state.db.update_or_create_data(STAFF_T, {'user_id': int(user_id)}, {gov_type: convert_bool_text(val)})


async def alist(state: State, from_user: User, params: list):
    """ Admin list """
    if params:
        await state.bot.send_message(from_user.id, 'This func cannot have any params')

    result = await state.db.get_data_all(STAFF_T)

    if not result:
        return "Admin list is empty."
    return str([i.user_id for i in result]).strip('[]')


def convert_bool_text(item: str):
    if item.lower() in ['true', '1']:
        return True
    return False

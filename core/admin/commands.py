import sys

from app.fitness.init import init_manage
from core.app import State


async def create_db():
    """ Initialize db from sql """
    state: State = await init_manage()
    if sys.argv[2:]:
        print('This func cannot have any params')
        return
    with open('core/db/sql/create_db.sql') as fd:
        await state.db.execute_many(fd.read())


async def create_admin():
    state: State = await init_manage()
    uid, admin, superadmin, *extra_args = sys.argv[2:]
    with open('core/db/sql_templates/add_admin.sql', 'r') as fd:
        sql = fd.read().format(
            user_id=int(uid),
            is_admin=_convert_terminal_bool(admin),
            is_superadmin=_convert_terminal_bool(superadmin)
        )
        await state.db.execute(sql)
    await state.shutdown()


def _convert_terminal_bool(item: str):
    """
    Converts terminal bool params to string format SQL
    """
    if item in ['True', 'true', '1']:
        return 'true'
    return 'false'

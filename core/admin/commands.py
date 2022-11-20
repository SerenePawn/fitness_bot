import sys
import logging

from app.fitness.init import init_manage
from core.app import State
from core.settings import (
    MIGRATIONS_FOLDER,
    SQL_TEMPLATES_FOLDER,
    SQL_TEMPLATES_FOLDER,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """ Initialize db from sql """
    state: State = await init_manage()
    if sys.argv[2:]:
        logger.warning('This func cannot have any params')
        return
    with open(f'{MIGRATIONS_FOLDER}/!init_db.sql') as fd:
        await state.db.execute_many(fd.read())


async def create_admin():
    state: State = await init_manage()
    uid, admin, superadmin, *extra_args = sys.argv[2:]
    with open(f'{SQL_TEMPLATES_FOLDER}/add_admin.sql', 'r') as fd:
        sql = fd.read().format(
            user_id=int(uid),
            is_admin=_convert_terminal_bool(admin),
            is_superadmin=_convert_terminal_bool(superadmin)
        )
        await state.db.execute(sql)
    await state.shutdown()


async def migrate():
    """ Migrate sql """
    state: State = await init_manage()
    migration_file, *extra_args = sys.argv[2:]
    try:
        with open(f'{MIGRATIONS_FOLDER}/{migration_file}', 'r') as fd:
            sql = fd.read()
            await state.db.execute(sql)
    except FileNotFoundError:
        logger.warning(f'Cannot find file')
    await state.shutdown()


def _convert_terminal_bool(item: str):
    """
    Converts terminal bool params to string format SQL
    """
    if item.lower() in ['true', '1']:
        return 'true'
    return 'false'

import asyncio
import sys
import logging

from core.admin import (
    MANAGE_CMDS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    try:
        manage_cmd = MANAGE_CMDS[sys.argv[1]]
    except KeyError:
        cmd_keys = ", ".join([
            f"\"manage.py {k}"
            f"{' ' + v['struct'] if v['struct'] else ''}\"" for k, v in MANAGE_CMDS.items()
        ])
        logger.warning(f'Wrong command "{sys.argv[1]}". Use one of the listed cmds: {cmd_keys}')
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(manage_cmd['cmd']())
        logger.info('Done.')

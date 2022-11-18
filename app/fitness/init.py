from core.app import State
from aiogram import executor
import asyncio
import logging
from core.settings import API_TOKEN
from .api.fitness import (
    register_dp_funcs,
    send_notify
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    app = State(API_TOKEN)

    try:
        register_dp_funcs(state=app)
        executor.start(
            app.dp,
            app.init(),
        )

        async def on_startup_bg(*args):
            return asyncio.create_task(
                send_notify(app)
            )

        executor.start_polling(
            app.dp,
            skip_updates=True,
            on_startup=on_startup_bg
        )
    except (GeneratorExit, asyncio.CancelledError):
        executor.start
    except Exception as e:
        logger.error(f'Fatal error: {e}')
        executor.start(app.dp, app.shutdown())

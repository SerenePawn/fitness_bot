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


def init(
    on_startup: callable = None,
    on_shutdown: callable = None
):
    app = State(API_TOKEN)

    def on_startup_bg(dp):
        return asyncio.create_task(
            send_notify(app)
        )

    try:
        register_dp_funcs(state=app)
        executor.start(
            app.dp,
            app.init(),
            # on_startup=on_startup_bg,
            # on_shutdown=on_shutdown
        )
        # TODO
        # loop = asyncio.get_event_loop()
        # asyncio.run_coroutine_threadsafe(send_notify(), loop)
        # executor.(
        #     app.dp,
        #     send_notify(app)
        # )
        executor.start_polling(app.dp, skip_updates=True)
    except (GeneratorExit, asyncio.CancelledError):
        executor.start
    except Exception as e:
        logger.error(f'Fatal error: {e}')
        executor.start(app.dp, app.shutdown())

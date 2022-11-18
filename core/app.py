from core.db.core_db import DatabaseManager
from templates.loader import LangManager as LM
from aiogram import (
    Bot,
    Dispatcher
)


class State:
    def __init__(self, token: str):
        self.db: DatabaseManager = DatabaseManager()
        self.lang_mgr: LM = LM()
        self.bot: Bot = Bot(token=token)
        self.dp: Dispatcher = Dispatcher(self.bot)

    async def init(self):
        await self.db.init_connection()

    async def shutdown(self):
        await self.db.shutdown()

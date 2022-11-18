from core.db.core_db import DatabaseManager
from core.db.models_db import SimplifiedQueries
from templates.loader import LangManager as LM
from aiogram import (
    Bot,
    Dispatcher
)


class State:
    def __init__(self, token: str):
        self.db_mgr: DatabaseManager = DatabaseManager()
        self.sq: SimplifiedQueries = SimplifiedQueries(self.db_mgr)
        self.lang_mgr: LM = LM()
        self.bot: Bot = Bot(token=token)
        self.dp: Dispatcher = Dispatcher(self.bot)

    async def init(self):
        await self.db_mgr.init_connection()

    async def shutdown(self):
        await self.db_mgr.shutdown()

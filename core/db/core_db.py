from databases import Database
from databases.backends.postgres import Record
from typing import Union
import logging

from core.settings import (
    POSTGRES_PASSWD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    conn: Database
    connected: bool = False

    def __init__(
        self,
        db_link: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    ):
        self.db_link = db_link

    async def init_connection(self):
        if self.connected:
            return self.connected

        self.conn = Database(self.db_link)

        await self.conn.connect()

        self.connected = True

        return self.connected

    async def shutdown(self):
        await self.conn.disconnect()
        logger.warning(f'Disconnected from db')

    async def execute(self, sql: str):
        db = self.conn
        await db.execute(sql)

    async def execute_many(self, sql: str, values: list[dict] | None = None):
        if values is None:
            values = [{}]
        db = self.conn
        await db.execute_many(sql, values)

    async def insert_data(self, table: str, **data: dict) -> Record:
        db = self.conn
        keys = data.keys()

        sql = f'''
            INSERT INTO {table} ({', '.join(keys)})
            VALUES ({', '.join([f":{i}" for i in keys])})
            RETURNING *
        '''

        res = await db.execute(sql, data)
        return res

    async def update_data(self, table: str, where: str, **data: dict) -> Record:
        db = self.conn
        do_not_update_id = data.pop('id')
        keys = data.keys()

        sql = f'''
            UPDATE {table}
            SET {', '.join([f'{i} = :{i}' for i in keys])}
            WHERE {where}
            RETURNING *
        '''

        data.update({'id': do_not_update_id})

        res = await db.execute(sql, data)
        return res

    async def get_data_all(self, table: str, where: str = '', order_by: str = '', **data) -> list[Record]:
        db = self.conn
        where = await self.__format_extra_opts('WHERE', where)
        order_by = await self.__format_extra_opts('ORDER BY', order_by)

        sql = f'''
            SELECT * FROM {table}
            {where}
            {order_by}
        '''

        res = await db.fetch_all(sql, data)

        return res

    async def get_data(self, table: str, where: str = '', **data: dict) -> Record:
        db = self.conn
        where = await self.__format_extra_opts('WHERE', where)

        sql = f'''
            SELECT * FROM {table}
            {where}
        '''

        res = await db.fetch_one(sql, data)

        return res

    async def exists_data(self, table: str, where: str = '', **data: dict) -> bool:
        db = self.conn
        where = await self.__format_extra_opts('WHERE', where)

        sql = f'''
            SELECT EXISTS(
                SELECT * FROM {table}
                {where}
            )
        '''

        res = await db.fetch_one(sql, data)

        return dict(res).get('exists')

    async def delete_data(self, table: str, where: str, **data: dict):
        db = self.conn

        sql = f'''
            DELETE FROM {table}
            WHERE {where}
        '''

        await db.fetch_one(sql, data)

    @staticmethod
    async def __format_extra_opts(opt: str, val: str) -> str:
        return f'{opt} {val}' if val != '' else val

from databases import Database
from databases.backends.postgres import Record
from typing import (
    Union,
    Any,
    List
)
import logging
from pydantic import BaseModel

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

    async def execute_many(self, sql: str, values: List[dict] | None = None):
        if values is None:
            values = [{}]
        db = self.conn
        await db.execute_many(sql, values)

    async def insert_data(self, table: str, data: dict) -> Record:
        db = self.conn
        data = self.__mtd(data)
        keys = data.keys()

        sql = f'''
            INSERT INTO {table} ({', '.join(keys)})
            VALUES ({', '.join([f":{i}" for i in keys])})
            RETURNING *
        '''

        res = await db.execute(sql, data)
        return res

    async def update_data(
        self,
        table: str,
        where: dict[str, Any] | BaseModel = {},
        upd_data: dict[str, Any] | BaseModel = {}
    ) -> Record:
        db = self.conn
        where = self.__mtd(where)
        upd_data = self.__mtd(upd_data)
        where_keys = where.keys()
        upd_keys = upd_data.keys()

        sql = f'''
            UPDATE {table}
            SET {', '.join([f'{i} = :upd_{i}' for i in upd_keys])}
            WHERE {' AND '.join([f'{i} = :wh_{i}' for i in where_keys])}
            RETURNING *
        '''

        query_data = dict([
            (f"wh_{k}", v) for k, v in where.items()
        ] + [
            (f"upd_{k}", v) for k, v in upd_data.items()
        ])

        res = await db.fetch_all(sql, query_data)
        return res

    async def get_data_all(
        self,
        table: str,
        where: dict[str, Any] | BaseModel = {},
        order_by: List[str] = []
    ) -> List[Record]:
        db = self.conn
        where = self.__mtd(where)
        where_query = await self.__format_extra_opts(
            'WHERE',
            ' AND '.join([f'{i} = :{i}' for i in where.keys()])
        )
        order_by = await self.__format_extra_opts(
            'ORDER BY',
            ', '.join([i for i in order_by])
        )

        sql = f'''
            SELECT * FROM {table}
            {where_query}
            {order_by}
        '''

        res = await db.fetch_all(
            sql,
            where
        )

        return res

    async def get_data(self, table: str, where: dict[str, Any] | BaseModel) -> Record:
        db = self.conn
        where = self.__mtd(where)
        where_query = await self.__format_extra_opts(
            'WHERE',
            ' AND '.join([f'{i} = :{i}' for i in where.keys()])
        )

        sql = f'''
            SELECT * FROM {table}
            {where_query}
        '''

        res = await db.fetch_one(sql, where)

        return res

    async def exists_data(
        self,
        table: str,
        where: dict[str, Any] | BaseModel = {}
    ) -> bool:
        db = self.conn
        where = self.__mtd(where)
        where_query = await self.__format_extra_opts(
            'WHERE',
            ' AND '.join([f'{i} = :{i}' for i in where.keys()])
        )

        sql = f'''
            SELECT EXISTS(
                SELECT * FROM {table}
                {where_query}
            )
        '''

        res = await db.fetch_one(sql, where)

        return dict(res).get('exists')

    async def delete_data(
        self,
        table: str,
        where: dict[str, Any] | BaseModel = {}
    ):
        db = self.conn
        where = self.__mtd(where)
        where_query = await self.__format_extra_opts(
            'WHERE',
            ' AND '.join([f'{i} = :{i}' for i in where.keys()])
        )

        sql = f'''
            DELETE FROM {table}
            WHERE {where_query}
        '''

        await db.fetch_one(sql, where)

    @staticmethod
    def record_to_mdl(record: Record, model: BaseModel) -> BaseModel:
        if not issubclass(model, BaseModel):
            raise TypeError
        return model(**record)

    @staticmethod
    def record_to_mdls(records: Record, model: BaseModel) -> BaseModel:
        if not issubclass(model, BaseModel):
            raise TypeError
        return [model(**i) for i in records]

    @staticmethod
    async def __format_extra_opts(opt: str, val: str) -> str:
        return f'{opt} {val}' if val != '' else val

    @staticmethod
    def __mtd(model_or_dict: BaseModel | dict):
        # Model to dict function
        if issubclass(type(model_or_dict), BaseModel):
            return model_or_dict.dict(exclude_none=True)
        return model_or_dict

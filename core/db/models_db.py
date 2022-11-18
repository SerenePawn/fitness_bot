from databases.backends.postgres import Record
from typing import (
    List,
    Any
)

from core.models.base.common import BaseCommonModel
from core.db.core_db import DatabaseManager


class SimplifiedQueries:
    def __init__(self, mgr: DatabaseManager):
        self.mgr = mgr

    async def exists_model(
        self,
        table: str,
        model: BaseCommonModel,
        **where: str
    ) -> bool:
        where_mdl = await self.__format_opts_old(model)
        where = await self.__format_opts_old(where)

        data = model.dict(exclude_none=True)
        data.update(where)

        return await self.mgr.exists_data(
            table,
            where + where_mdl,
            **data
        )

    async def get_common_model(
        self,
        table: str,
        model: BaseCommonModel,
        **where: str
    ) -> Record:
        where_mdl = await self.__format_opts_old(model)
        where = await self.__format_opts_old(where)

        data = model.dict(exclude_none=True)
        data.update(where)

        return await self.mgr.get_data(
            table,
            where + where_mdl,
            **data
        )

    async def get_common_models(
        self,
        table: str,
        model: BaseCommonModel,
        order_by: List[str] = [],
        **where: str
    ) -> List[Record]:
        where_mdl = await self.__format_opts_old(model)
        where = await self.__format_opts_old(where)
        order_by = ', '.join([i for i in order_by])

        data = model.dict(exclude_none=True)
        data.update(where)

        return await self.mgr.get_data_all(
            table,
            where + where_mdl,
            order_by,
            **data
        )

    async def insert_model(
        self,
        table: str,
        model: BaseCommonModel,
        **extra_data: str
    ):
        data = model.dict(exclude_none=True)
        data.update(extra_data)

        return await self.mgr.insert_data(
            table,
            **data
        )

    async def update_model(
        self,
        table: str,
        model: BaseCommonModel,
        exclude_where: List[str],
        **where: str
    ) -> Record:
        # OBSOLETE
        where_mdl = await self.__format_opts_old(model, exclude_where=exclude_where)
        where = await self.__format_opts_old(where, exclude_where=exclude_where)

        data = model.dict(exclude_none=True)
        data.update(where)

        return await self.mgr.update_data(
            table,
            where + where_mdl,
            **data
        )

    async def update_record(
        self,
        table: str,
        where: dict[str, Any],
        **data
    ) -> Record:
        _where, where_data = await self.__format_opts(where)

        data.update(where)

        return await self.mgr.update_data(
            table,
            _where,
            **data
        )

    async def delete_model(
        self,
        table: str,
        model: BaseCommonModel,
        **where: str
    ):
        where_mdl = await self.__format_opts_old(model)
        where = await self.__format_opts_old(where)

        data = model.dict(exclude_none=True)
        data.update(where)

        return await self.mgr.delete_data(
            table,
            where + where_mdl,
            **data
        )

    @staticmethod
    async def __format_opts_old(
        opt: dict[str, Any] | BaseCommonModel,
        exclude_where: List[str] = []
    ) -> str:
        if not opt:
            return ''

        mdl_fields = opt.dict(exclude_none=True).keys()
        return ' AND '.join([f'{i} = :{i}' for i in mdl_fields if i not in exclude_where])

    @staticmethod
    async def __format_opts(
        opt: dict[str, Any]
    ) -> str:
        if not opt:
            return ''

        keys = opt.keys()
        vals = opt.values()
        where_str = ' AND '.join([f'{i} = :{i}' for i in keys])
        return where_str, vals

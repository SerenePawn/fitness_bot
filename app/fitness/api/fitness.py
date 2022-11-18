import logging
from aiogram import types
from datetime import (
    datetime, timedelta
)
import asyncio
from time import time

import core.models.fitness.models as mdl
from core.enums.enums import UserStatusEnum
from core.enums.admin import AdminCmdsEnum
from core.settings import (
    STARTUP_TIME,
    ADMIN_USERNAMES_ALLOWED,
    ADMIN_PASSWD
)
from core.app import State


logger = logging.getLogger(__name__)


USERS_T = 'users'
WEIGHING_T = 'weighing'
STAFF_T = 'staff'


def register_dp_funcs(state: State):
    """
    Registering all fitness bot funcs.
    """

    @state.dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        lang_code = message.from_user['language_code']
        user_registered = await state.sq.exists_model(
            USERS_T,
            mdl.UserSearchUpdateModel(id=message.from_id)
        )

        if user_registered:
            await message.reply(
                await state.lang_mgr.load_phrase('already_started', lang_code)
            )
            return
        await message.reply(
            await state.lang_mgr.load_phrase(
                'start_hello',
                lang_code,
                first_name=message.from_user.first_name
            )
        )

    @state.dp.message_handler(regexp=r'^\d{2,3}$')
    async def send_wished_weight(message: types.Message):
        from_id = message.from_id
        lang_code = message.from_user['language_code']
        user_weighing_started = await state.sq.exists_model(
            USERS_T,
            mdl.UserSearchUpdateModel(id=from_id)
        )
        if user_weighing_started:
            await message.reply(
                await state.lang_mgr.load_phrase('please_current_weight', lang_code)
            )
            return

        await state.sq.insert_model(
            USERS_T,
            mdl.UserModel(
                id=from_id,
                weight_wished=int(message.text),
                status=UserStatusEnum.WITH_WISHES,
                lang_code=lang_code
            )
        )

        await message.reply(
            await state.lang_mgr.load_phrase('send_current_weight', lang_code, weight=message.text)
        )

    @state.dp.message_handler(regexp=r'^\d{2,3}, \d{2}\.\d{2}\.\d{4}$')
    async def send_weghing(message: types.Message):
        model = mdl.UserSearchUpdateModel(id=message.from_id)
        user = mdl.UserModel(
            **await state.sq.get_common_model(
                USERS_T,
                model
            )
        )

        lang_code = message.from_user['language_code']
        weight, date = message.text.split(', ')
        weight = int(weight)
        day, month, year = [int(i) for i in date.split('.')]
        date = datetime(year=year, month=month, day=day)

        if user:
            if user.weight_wished >= weight:
                await message.reply(
                    await state.lang_mgr.load_phrase('hooray', lang_code)
                )
                await model.delete()
                return

            await state.sq.insert_model(
                WEIGHING_T,
                mdl.WeighingModel(
                    user_id=user.id,
                    weight=weight,
                    ctime=date
                )
            )

            # await state.sq.update_model(
            #     USERS_T,
            #     mdl.UserSearchUpdateModel(
            #         id=user.id,
            #         status=UserStatusEnum.IN_PROGRESS
            #     ),
            #     exclude_where=['status']
            # )

            await state.sq.update_record(
                USERS_T,
                dict(
                    id=user.id
                ),
                status=UserStatusEnum.IN_PROGRESS,
                id=user.id,
            )

            await message.reply(
                await state.lang_mgr.load_phrase(
                    'last_weight_was',
                    lang_code,
                    weight=weight,
                    date=date.date()
                )
            )
        else:
            await message.reply(
                await state.lang_mgr.load_phrase('send_wished', lang_code)
            )

    @state.dp.message_handler(commands=['schedule'])
    async def send_schedule(message: types.Message):
        lang_code = message.from_user['language_code']
        from_id = message.from_id
        weighing = await state.sq.get_common_models(
            WEIGHING_T,
            mdl.WeighingSearchUpdateModel(
                user_id=from_id
            ),
            ['ctime']
        )
        result = await state.lang_mgr.load_phrase('your_schedule', lang_code)

        if not weighing:
            await message.reply(
                await state.lang_mgr.load_phrase('not_started', lang_code)
            )
            return

        # Send all data with filling where weighing skipped
        last_date = weighing[0].ctime.date()
        last_weight = 0
        for i in weighing:
            next_date = i.ctime.date()
            offset_date = timedelta(days=1)
            last_date += offset_date
            while last_date < next_date:
                result += await state.lang_mgr.load_phrase(
                    'line_schedule',
                    lang_code,
                    weight=last_weight,
                    date=last_date
                )
                last_date += offset_date

            result += await state.lang_mgr.load_phrase(
                'line_schedule',
                lang_code,
                weight=i.weight,
                date=i.ctime.date()
            )
            last_date = i.ctime.date()
            last_weight = i.weight

        await message.reply(result)

    @state.dp.message_handler(commands=['admin'], regexp=r'/admin .+ .+')
    async def send_admin(message: types.Message):
        """
        Simple admin panel in text chat.
        """
        from_user = message.from_user
        _, passwd, cmd, *extra = message.text.split(' ')
        cmd = cmd.lower()
        await message.delete()

        if not passwd == ADMIN_PASSWD or from_user.username not in ADMIN_USERNAMES_ALLOWED:  # TODO
            await state.bot.send_message(
                from_user.id,
                'Invalid password. If you\'re not an admin, you\'ve been banned after a few attempts.'
            )
            return

        if cmd not in AdminCmdsEnum.CMDS.keys():
            # Reminder: only for create_db.
            await state.bot.send_message(from_user.id, 'Invalid command.')
            return

        # execute enum-ed cmd.
        await AdminCmdsEnum.CMDS[cmd](state.db_mgr, extra)
        await state.bot.send_message(from_user.id, 'Ok.')


async def send_notify(state: State):
    """
    Its working worse. Need TODO:
        - Make asyncio sleep like: 
            wakeup -> check time is come -> sleep for the time to next wake up
        - Make user's TZ to sync time
            So to do this need to make list of users who already got msg
            And save users TZ to db
    """
    hour, minute = STARTUP_TIME
    while True:
        await asyncio.sleep(
            await check_time_to_sleep(hour, minute)
        )
        print('!!!!!!!!!!!!!', await check_time_to_sleep(hour, minute))

        users = await state.sq.get_common_models(
            USERS_T,
            mdl.UserSearchUpdateModel(
                status=UserStatusEnum.IN_PROGRESS
            )
        )

        for i in users:
            await state.bot.send_message(
                i.id,
                await state.lang_mgr.load_phrase('weighting_time', i.lang_code)
            )


async def check_time_to_sleep(hour: int, minute: int) -> float:
    time_now = datetime.now()
    time_dest = time_now.replace(hour=hour, minute=minute)

    if time_dest - time_now < timedelta(0):
        time_dest.replace(day=time_dest.day + 1)

    return (time_dest - time_now).total_seconds()

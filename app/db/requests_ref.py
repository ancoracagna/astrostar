import datetime

from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select, update, delete

from app.db.models import async_session, OP, Setting


async def get_settings_ref_status():
    async with async_session() as session:
        ref_status = await session.scalar(select(Setting.reff_enabled))
        return ref_status

async def switch_settings_ref():
    async with async_session() as session:
        ref_status = await get_settings_ref_status()
        new_ref = 0
        if int(ref_status) == 1:
            new_ref = 0
        else:
            new_ref = 1
        user_update = (
            update(Setting)
                .where(Setting.reff_enabled == ref_status)
                .values(reff_enabled=new_ref)
        )
        await session.execute(user_update)
        await session.commit()

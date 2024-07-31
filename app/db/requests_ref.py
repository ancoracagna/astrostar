import datetime

from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select, update, delete, func, distinct

from app.db.models import async_session, OP, Setting, EventRef, Ref_Code, User


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

async def get_all_refs_starts(ref_name: str):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(distinct(EventRef.tg_id)))
            .where(EventRef.ref_name == ref_name)
        )
        all_refs_starts = result.scalar()
        return all_refs_starts


async def get_ops_list(ref_name):
    async with async_session() as session:
        ops_list = await session.scalar(select(Ref_Code.users_op).where(Ref_Code.ref_name == ref_name))
        return ops_list


async def add_user_op_toref(tg_id, ref_name):
    async with async_session() as session:
        ops_list = await get_ops_list(ref_name)

        if ops_list:
            ops_list = ops_list.split(',')
        else:
            ops_list = []

        # Добавляем новый tg_id в список, если его там еще нет
        if str(tg_id) not in ops_list:
            ops_list.append(str(tg_id))

        # Преобразуем список обратно в строку
        updated_ops_list = ','.join(ops_list)

        # Обновляем запись в базе данных
        await session.execute(
            update(Ref_Code)
                .where(Ref_Code.ref_name == ref_name)
                .values(users_op=updated_ops_list)
        )
        await session.commit()

        print(f'Updated ops_list: {updated_ops_list}')
        return updated_ops_list

async def get_refs_unique(ref_name: str):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(EventRef.id))
            .where(EventRef.ref_name == ref_name, EventRef.event == 'newuser')
        )
        refs_unique = result.scalar()
        return refs_unique

async def get_user_ref(tg_id):
    async with async_session() as session:
        ref = await session.scalar(select(User.refer_id).where(User.tg_id == tg_id))
        return ref

async def get_op_users(ref_name: str) -> int:
    async with async_session() as session:
        ops_lst = await get_ops_list(ref_name)

        if ops_lst:
            # Разделяем строку на элементы и убираем лишние пробелы, если они есть
            ops_lst = ops_lst.split(',')
            ops_lst = [tg_id.strip() for tg_id in ops_lst]
        else:
            ops_lst = []

        return len(ops_lst)
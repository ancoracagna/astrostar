import datetime

from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select, update, delete

from app.db.models import async_session, OP, Setting


async def create_op(tg_id, name, username, link):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        ref = await session.scalar(select(OP).where(OP.op_name == name))
        if not ref:
            session.add(OP(tg_id=tg_id, op_name=name, op_username=username, op_link=link, op_status='0', op_count=0, op_date=d1,
                           op_tgs='111,222'))
            await session.commit()
        else:
            return 0


PAGE_SIZE = 5  # Количество элементов на странице


async def get_op_lst(page: int = 1):
    async with async_session() as session:
        offset = (page - 1) * PAGE_SIZE
        result = await session.execute(
            select(OP.op_name).order_by(OP.op_date.desc()).offset(offset).limit(PAGE_SIZE) # вместо asc - desc
        )
        all_op_codes = [row[0] for row in result.fetchall()]
        return all_op_codes

async def get_op_data(op_name: str):
    async with async_session() as session:
        op_data = await session.scalar(select(OP).where(OP.op_name == op_name))
        if op_data:
            return op_data


async def get_actual_op():
    async with async_session() as session:
        op_lst = []
        ops = await session.scalars(select(OP.op_username).where(OP.op_status == '1'))
        print(f'ops: {ops}')
        return ops

async def get_actual_op_full():
    async with async_session() as session:
        op_lst = []
        ops = await session.scalars(select(OP).where(OP.op_status == '1'))
        print(f'ops: {ops}')
        return ops

async def check_op(user, bot):
    actual_op = await get_actual_op()
    negative = 0
    for op in actual_op:
        user_channel_status = await bot.get_chat_member(chat_id=op, user_id=user) # op здесь это channel_id
                                                                                  # который должен быть записан где то
        if user_channel_status["status"] != 'left':
           pass
        else:
           negative+=1

    if negative != 0:
        return 0
    else:
        return 1

async def check_bot_channel_admin(bot):
    actual_op = await get_actual_op()
    badlst = []
    for op in actual_op:
        try:
            #op = op.replace('t.me/', '@') # Это если ссылка через t.me/genesisgang а если https://t.me/+PjDRRsNifus4ZmQy
            user_channel_status = await bot.get_chat_member(user_id=709495509, chat_id=op)
            print(f'actuap_op: {op}')
            print(f'status: {user_channel_status.status}')
        except TelegramBadRequest as exception:
            #op = op.replace('t.me/', '@')
            badlst.append(op)
            print(exception)
    return badlst

async def switch_status_op(op_name):
    async with async_session() as session:
        data = await get_op_data(op_name)
        status = data.op_status
        if int(status) == 0:
            status = 1
        else:
            status = 0
        user_update = (
            update(OP)
                .where(OP.op_name == op_name)
                .values(op_status=status)
        )
        await session.execute(user_update)
        await session.commit()

async def switch_status_op_by_username(op_username):
    async with async_session() as session:
        user_update = (
            update(OP)
                .where(OP.op_username == op_username)
                .values(op_status=0)
        )
        await session.execute(user_update)
        await session.commit()

async def delete_op_req(name):
    async with async_session() as session:
        print(f'OP_NAME: {name}')
        stmt = delete(OP).where(OP.op_name == name)
        print(stmt)
        await session.execute(stmt)
        await session.commit()

async def get_settings_op_status():
    async with async_session() as session:
        op_status = await session.scalar(select(Setting.op_enabled))
        return op_status

async def switch_settings_op():
    async with async_session() as session:
        op_status = await get_settings_op_status()
        new_op = 0
        if int(op_status) == 1:
            new_op = 0
        else:
            new_op = 1
        user_update = (
            update(Setting)
                .where(Setting.op_enabled == op_status)
                .values(op_enabled=new_op)
        )
        await session.execute(user_update)
        await session.commit()


async def get_name_by_username(username):
    async with async_session() as session:
        name = await session.scalar(select(OP.op_name).where(OP.op_username == username))
        return name

async def get_link_by_username(username):
    async with async_session() as session:
        link = await session.scalar(select(OP.op_link).where(OP.op_username == username))
        return link
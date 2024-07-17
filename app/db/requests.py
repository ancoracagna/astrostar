import datetime
from app.db.models import async_session
from app.db.models import User, Check, Forecast, Event, Ref_Code, EventRef
from sqlalchemy import and_, func
from sqlalchemy import select, update


async def set_user(tg_id, refer_id):
    async with async_session() as session:
        today = datetime.date.today()
        print(f'ref: {refer_id}')
        d1 = today.strftime("%d/%m/%Y")
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, refs=0, refer_id=str(refer_id), date=d1))
            await session.commit()

async def add_ref_event(tg_id, event, ref_name):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        session.add(EventRef(tg_id=tg_id, event=event, date=d1, ref_name=ref_name))
        await session.commit()

async def add_check(tg_id, desc, res, unique):
    async with async_session() as session:
        session.add(Check(tg_id=tg_id, desc=desc, res=res, unique=unique))
        await session.commit()


async def get_check(unique):
    async with async_session() as session:
        result = await session.execute(select(Check.res).where(Check.unique == unique))
        print(f'unique: {unique}')
        row = result.fetchone()

        if row is not None:
            resultres = row[0]
            print(f'result: {result} resultres: {resultres}')
            return resultres
        else:
            return None  # Или другое значение по умолчанию, если ничего не найдено


async def get_refs(tg_id):
    async with async_session() as session:
        refs = await session.scalar(select(User.refs).where(User.tg_id == tg_id))
        return refs

async def get_ref_market(code):
    async with async_session() as session:
        #refs = await session.scalar(select(User.refs).where(User.refer_id == code))
        result = await session.execute(select(func.count(User.refer_id)).where(User.refer_id == code))
        refs = result.scalar()
        return refs

async def get_ref_unique(code):
    async with async_session() as session:
        #refs = await session.scalar(select(User.refs).where(User.refer_id == code))
        result = await session.execute(select(func.count(EventRef.ref_name)).where(and_(EventRef.ref_name == code, EventRef.event == 'newuser')))
        refs = result.scalar()
        return refs

async def get_all_ref_starts(code):
    async with async_session() as session:
        #refs = await session.scalar(select(User.refs).where(User.refer_id == code))
        result = await session.execute(select(func.count(EventRef.ref_name)).where(EventRef.ref_name == code))
        refs = result.scalar()
        return refs

async def get_today_refs(code):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        result = await session.execute(select(func.count(User.refer_id)).where(and_(User.date == d1, User.refer_id == code)))
        today_users = result.scalar()
        return today_users

async def get_week_refs(code):
    async with async_session() as session:
        start_date = datetime.date.today() - datetime.timedelta(7)
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        count = 0
        while start_date < today:
            start_date = start_date + datetime.timedelta(days=1)
            print(f'date: {start_date}')
            d1 = start_date.strftime("%d/%m/%Y")
            result = await session.execute(select(func.count(User.refer_id)).where(and_(User.date == d1, User.refer_id == code)))
            count += result.scalar()
        return count

async def get_month_refs(code):
    async with async_session() as session:
        start_date = datetime.date.today() - datetime.timedelta(30)
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        count = 0
        while start_date < today:
            start_date = start_date + datetime.timedelta(days=1)
            print(f'date: {start_date}')
            d1 = start_date.strftime("%d/%m/%Y")
            result = await session.execute(select(func.count(User.refer_id)).where(and_(User.date == d1, User.refer_id == code)))
            count += result.scalar()
        return count

async def check_ref_code(code):
    async with async_session() as session:
        ref = await session.scalar(select(Ref_Code).where(Ref_Code.ref_name == code))
        if not ref:
            return 0

async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(func.count(User.id)))
        all_users = result.scalar()
        return all_users

async def create_ref_code(tg_id, ref_name, price):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        ref = await session.scalar(select(Ref_Code).where(Ref_Code.ref_name == ref_name))
        if not ref:
            session.add(Ref_Code(tg_id=tg_id, ref_name=ref_name, price=price, date=d1))
            await session.commit()
        else:
            return 0

async def get_ref_price(ref_name):
    async with async_session() as session:
        price = await session.scalar(select(Ref_Code.price).where(Ref_Code.ref_name == ref_name))
        return price


async def get_all_users_lst():
    async with async_session() as session:
        result = await session.execute(select(User.tg_id))
        all_users = [row[0] for row in result.fetchall()]  # Извлекаем первый столбец из всех строк результата
        return all_users

PAGE_SIZE = 5  # Количество элементов на странице

async def get_ref_lst(page: int = 1):
    async with async_session() as session:
        offset = (page - 1) * PAGE_SIZE
        result = await session.execute(
            select(Ref_Code.ref_name).order_by(Ref_Code.date.desc()).offset(offset).limit(PAGE_SIZE)
        )
        all_reff_codes = [row[0] for row in result.fetchall()]
        return all_reff_codes

async def get_today_users():
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        result = await session.execute(select(func.count(User.id)).where(User.date == d1))
        today_users = result.scalar()
        return today_users


async def get_month_users():
    async with async_session() as session:
        start_date = datetime.date.today() - datetime.timedelta(30)
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        count = 0
        while start_date < today:
            start_date = start_date + datetime.timedelta(days=1)
            print(f'date: {start_date}')
            d1 = start_date.strftime("%d/%m/%Y")
            result = await session.execute(select(func.count(User.id)).where(User.date == d1))
            count += result.scalar()
        return count


async def get_user_data(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user


async def add_ref(tg_id):
    async with async_session() as session:
        async with session.begin():
            # Выполнение селект-запроса для получения текущего значения
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            user = result.scalar_one_or_none()

            if user is not None:
                # Увеличение значения в столбце refer_id на 1
                user.refs += 1
                session.add(user)
                await session.commit()
            else:
                print(f"User with tg_id {tg_id} not found")


async def get_horoscope():
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        result = await session.execute(select(Forecast.desc).where(Forecast.date == d1))
        row = result.fetchone()
        if row is not None:
            resultres = row[0]
            print(f'result: {result} resultres: {resultres}')
            return resultres


async def get_event_count(type):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        event_count = await session.scalar(select(Event.count).where(and_(Event.type == type, Event.date == d1)))
        return event_count


async def check_available_event(type):
    async with async_session() as session:
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        result = await session.scalar(
            select(Event).where(
                and_(
                    Event.type == type,
                    Event.date == d1
                )
            )
        )
        if not result:
            session.add(Event(type=type, count=0, date=d1))
            await session.commit()


async def reg_event(type):
    async with async_session() as session:
        await check_available_event(type)
        today = datetime.date.today()
        d1 = today.strftime("%d/%m/%Y")
        curr = await get_event_count(type)
        new_count = int(curr) + 1
        user_update = (
            update(Event)
                .where(and_(Event.type == type, Event.date == d1))
                .values(count=new_count)
        )
        await session.execute(user_update)
        await session.commit()

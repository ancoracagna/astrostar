import asyncio
from create_bot import bot, dp, admins


from app.db.models import async_main
from app.db.requests import get_all_users
from app.handlers.admin_handler import admin_router as admin
from app.handlers.user_handler import router as user

from app.filters.main_filter import ADMINS as admins

async def main():

    dp.include_routers(admin, user)
    dp.startup.register(on_startup)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)


async def on_startup(dispatcher):
    await async_main()
    count_users = await get_all_users()
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущен🥳. \nСейчас в базе данных {count_users} пользователей.')
    except:
        pass



# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass

if __name__ == '__main__':
    asyncio.run(main())

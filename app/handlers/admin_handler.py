import re

from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from app.builder import ref_code_key, ref_keys_builder
from app.db.requests import get_all_users, get_today_users, get_all_users_lst, get_month_users, get_event_count, \
    get_ref_market, create_ref_code, get_ref_lst
from app.filters.main_filter import AdminProtect
from app.keyboards import adminpanel, apanelback, apanelsendall, marketpanel, templatesend
from app.states import SendAllPic, SendAllText, Marketing, New_Ref, BroadcastState
from app.utils.utils import get_ref_info

admin_router = Router()


@admin_router.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message, command: Command):
    await message.answer('Вы зашли в панель администратора', reply_markup=adminpanel)


@admin_router.message(AdminProtect(), Command('stat'))
async def stat(message: Message, command: Command):
    await message.answer('Вы зашли в панель администратора')


@admin_router.message(AdminProtect(), Command('sendall'))
async def sendall(message: Message, command: Command):
    await message.answer('Вы зашли в панель администратора')


@admin_router.callback_query(AdminProtect(), F.data == 'marketing')
async def marketing(callback: CallbackQuery):
    await callback.answer('Вы перешли в раздел маркетинг')
    await callback.message.edit_text('Выберите меню из списка', reply_markup = marketpanel)

@admin_router.callback_query(AdminProtect(), F.data == 'create_ref_code')
async def create_refcode(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы перешли в раздел создания ссылки')
    await callback.message.edit_text('Введите реферальный код, пример "AGARIO"')
    await state.set_state(New_Ref.ref_name)
    # Здесь логика получения из бд + разбивать по 10 кодов, сделать переключение как в backet

@admin_router.message(AdminProtect(), New_Ref.ref_name)
async def marketing_getinfo(message: Message, state: FSMContext):
    await state.update_data(ref_name=message.text)
    await message.answer('Введите стоимость:')
    await state.set_state(New_Ref.price)


@admin_router.message(AdminProtect(), New_Ref.price)
async def setrefprice(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    ref_code = await state.get_data()
    ref_name = ref_code["ref_name"]
    ref_price = ref_code["price"]
    if await create_ref_code(message.from_user.id, ref_name, ref_price)!=0:
        await message.answer(f'Ссылка {ref_name} успешно создана!', reply_markup=ref_code_key(ref_name))
        await state.clear()
    else:
        await message.answer(f'Ссылка {ref_name} уже существует!')
        await state.clear()

@admin_router.callback_query(AdminProtect(), F.data.startswith('refcode_'))
async def inline_refcode(callback: CallbackQuery):
    ref_code = callback.data.split('_')[1]
    answer = await get_ref_info(ref_code)
    await callback.message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer(f'Вы запросили статистику по ссылке: {ref_code}')


@admin_router.callback_query(AdminProtect(), F.data.startswith('ref_code_lst'))
async def get_ref_codes(callback: CallbackQuery):
    page = 1  # Начинаем с первой страницы
    await send_ref_list(callback, page)

@admin_router.callback_query(AdminProtect(), F.data.startswith('back_reflist_'))
async def go_back(callback: CallbackQuery):
    current_page = int(callback.data.split('_')[-1])
    if current_page > 1:
        await send_ref_list(callback, current_page - 1)
    else:
        await callback.answer('Вы на первой странице', show_alert=True)

@admin_router.callback_query(AdminProtect(), F.data.startswith('forward_reflist_'))
async def go_forward(callback: CallbackQuery):
    current_page = int(callback.data.split('_')[-1])
    await send_ref_list(callback, current_page + 1)

async def send_ref_list(callback: CallbackQuery, page: int):
    ref_lst = await get_ref_lst(page)
    if ref_lst:
        await callback.message.edit_text(
            'Список ссылок по дате по убыванию',
            reply_markup=ref_keys_builder(ref_lst, page)
        )
    else:
        await callback.answer('Больше нет элементов', show_alert=True)

@admin_router.callback_query(AdminProtect(), F.data == 'manual_ref_search')
async def manual_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите реферальный код')
    await state.set_state(Marketing.ref_name)

@admin_router.message(AdminProtect(), Marketing.ref_name)
async def marketing_getinfo(message: Message, state: FSMContext):
    await state.update_data(ref_name=message.text)
    ref_code = await state.get_data()
    answer = await get_ref_info(ref_code["ref_name"])
    await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)


@admin_router.callback_query(AdminProtect(), F.data == 'stat')
async def get_stat(callback: CallbackQuery):
    await callback.answer('Статистика')
    month_users = await get_month_users()
    print(month_users)
    all_users = await get_all_users()
    today_users = await get_today_users()
    today_horoscope = await get_event_count('Гороскоп')
    today_comp = await get_event_count('Совместимость')
    await callback.message.edit_text(
        f'*\=\=\=\=\=\=\= Статистика \=\=\=\=\=\=\=*\n\n👥 Пользователей в системе: {all_users}\n'
        f'🆕 Новых сегодня: {today_users}\n'
        f'🗓 Новых за месяц: {month_users}\n'
        f'❤️ Запросов совместимости: {today_comp}\n'
        f'🔮 Запросов гороскопа: {today_horoscope}', parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=apanelback)


@admin_router.callback_query(AdminProtect(), F.data == 'sendall')
async def send_all(callback: CallbackQuery):
    await callback.answer('Рассылка')
    await callback.message.edit_text('Выберите вариант рассылки', reply_markup=apanelsendall)
    all_users = await get_all_users_lst()
    print(all_users)


@admin_router.callback_query(AdminProtect(), F.data == 'sendallpic')
async def send_all(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Рассылка с картинкой')
    await state.set_state(SendAllPic.img)
    await callback.message.edit_text('Пришлите картинку')


@admin_router.callback_query(AdminProtect(), F.data == 'sendalltxt')
async def send_all(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Рассылка текстом')
    await state.set_state(SendAllText.text)
    await callback.message.edit_text('Пришлите текст для рассылки')


@admin_router.message(AdminProtect(), SendAllText.text)
async def sendtxt(message: Message, state: FSMContext, bot: Bot):
    all_users = await get_all_users_lst()
    await state.update_data(text=message.text)
    data = await state.get_data()
    count = 0
    for user in all_users:
        try:
            await bot.send_message(user, text=data['text'])
            count += 1
        except:
            print('error')
    await message.answer(f'Рассылка охватила {count} пользователей')
    await state.clear()


@admin_router.message(AdminProtect(), SendAllPic.img)
async def addimgtosend(message: Message, state: FSMContext):
    await state.update_data(img=message.photo[-1].file_id)
    await state.set_state(SendAllPic.text)
    await message.answer('Пришлите текст для рассылки')  # Нужно сохранять форматирование я видел пример


@admin_router.message(AdminProtect(), SendAllPic.text)
async def sendall(message: Message, state: FSMContext, bot: Bot):
    all_users = await get_all_users_lst()
    await state.update_data(text=message.text)
    data = await state.get_data()
    count = 0
    for user in all_users:
        try:
            await bot.send_photo(user, photo=data['img'], caption=data['text'])
            count += 1
        except:
            print('error')
    await message.answer(f'Рассылка охватила {count} пользователей')
    await state.clear()


@admin_router.callback_query(AdminProtect(), F.data == 'back')
async def back_to_panel(callback: CallbackQuery):
    await callback.answer('Вы успешно вернулись')
    await callback.message.edit_text('Вы зашли в панель администратора', reply_markup=adminpanel)

@admin_router.callback_query(AdminProtect(), F.data == 'sendtemplate')
async def testmsg(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Перешлите шаблон')
    await callback.message.answer('Перешлите сообщение для рассылки')
    await state.set_state(BroadcastState.waiting_for_message)

@admin_router.message(AdminProtect(), BroadcastState.waiting_for_message)
async def sendformat(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(
        message_id=message.message_id,
        chat_id=message.chat.id,
        content_type=message.content_type,
        text=message.html_text if message.html_text else None,
        photo=message.photo[-1].file_id if message.photo else None,
        document=message.document.file_id if message.document else None,
        reply_markup=message.reply_markup
    )
    # Отображение сообщения
    if message.content_type == 'text':
        await bot.send_message(chat_id=message.chat.id, text=message.html_text, parse_mode=ParseMode.HTML, reply_markup=message.reply_markup)
    elif message.content_type == 'photo':
        await bot.send_photo(chat_id=message.chat.id, photo=message.photo[-1].file_id, caption=message.html_text, parse_mode=ParseMode.HTML, reply_markup=message.reply_markup)
    elif message.content_type == 'document':
        await bot.send_document(chat_id=message.chat.id, document=message.document.file_id, caption=message.html_text, parse_mode=ParseMode.HTML, reply_markup=message.reply_markup)

    await message.answer('Вы уверены, что хотите отправить это сообщение всем?', reply_markup=templatesend)
    await state.set_state(BroadcastState.confirm_message)

@admin_router.callback_query(AdminProtect(), BroadcastState.confirm_message, F.data == 'confirm_send')
async def sendtemplate(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    all_users = await get_all_users_lst()
    count = 0
    for user_id in all_users:
        try:
            if data['content_type'] == 'text':
                await bot.send_message(chat_id=user_id, text=data['text'], parse_mode=ParseMode.HTML, reply_markup=data['reply_markup'])
            elif data['content_type'] == 'photo':
                await bot.send_photo(chat_id=user_id, photo=data['photo'], caption=data['text'], parse_mode=ParseMode.HTML, reply_markup=data['reply_markup'])
            elif data['content_type'] == 'document':
                await bot.send_document(chat_id=user_id, document=data['document'], caption=data['text'], parse_mode=ParseMode.HTML, reply_markup=data['reply_markup'])
            count += 1
        except Exception as e:
            print(f'Не удалось отправить сообщение пользователю {user_id}: {e}')

    await callback.message.edit_text(f'Рассылка завершена! Сообщение отправлено {count} пользователям.')
    await state.clear()

@admin_router.callback_query(AdminProtect(), F.data == 'canceltemplate')
async def canceltemplate(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отмена')
    await callback.message.edit_text('Вы отменили рассылку', reply_markup=adminpanel)
    await state.clear()
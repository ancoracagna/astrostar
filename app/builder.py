from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.db.requests import check_user_subs
from app.db.requests_op import get_op_data, get_settings_op_status, get_actual_op, \
    get_actual_op_full, get_name_by_username, get_link_by_username
from app.db.requests_ref import get_settings_ref_status
from app.utils.utils import check_admin_channels


def ref_code_key(ref_code):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=ref_code, callback_data=f'refcode_{ref_code}'))
    return keyboard.adjust(1).as_markup()


def ref_keys_builder(refs_lst, current_page: int):
    keyboard = InlineKeyboardBuilder()

    for ref in refs_lst:
        keyboard.add(InlineKeyboardButton(text=ref, callback_data=f'refcode_{ref}'))

    navigation_buttons = [
        InlineKeyboardButton(text='⬅️', callback_data=f'back_reflist_{current_page}'),
        InlineKeyboardButton(text='➡️', callback_data=f'forward_reflist_{current_page}')
    ]

    keyboard.adjust(1).row(*navigation_buttons)

    return keyboard.as_markup()


def op_builder(name, link):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=name, url=link))

    return keyboard.as_markup()


def op_keys_builder(op_lst, current_page: int):
    keyboard = InlineKeyboardBuilder()

    for op in op_lst:
        keyboard.add(InlineKeyboardButton(text=op, callback_data=f'op_{op}'))

    navigation_buttons = [
        InlineKeyboardButton(text='⬅️', callback_data=f'back_oplist_{current_page}'),
        InlineKeyboardButton(text='➡️', callback_data=f'forward_oplist_{current_page}')
    ]

    keyboard.adjust(1).row(*navigation_buttons)

    return keyboard.as_markup()


async def op_switch_kb(name):
    keyboard = InlineKeyboardBuilder()

    data = await get_op_data(name)
    status = data.op_status
    status_str = 'Неизвестно'
    if int(status) == 0:
        status_str = '🔴 Выключена'
    else:
        status_str = '🟢 Включена'

    main_buttons = [InlineKeyboardButton(text=status_str, callback_data=f'switch_{name}'),
                    InlineKeyboardButton(text='Удалить', callback_data=f'delete_{name}')]

    keyboard.adjust(1).row(*main_buttons)

    return keyboard.as_markup()


async def settingbuilder():
    keyboard = InlineKeyboardBuilder()

    op_status = await get_settings_op_status()
    ref_status = await get_settings_ref_status()
    op_str = ''
    ref_str = ''
    if int(op_status) == 1:
        op_str = '🟢 ОП'
    if int(op_status) == 0:
        op_str = '🔴 ОП'
    if int(ref_status) == 1:
        ref_str = '🟢 Реф'
    if int(ref_status) == 0:
        ref_str = '🔴 Реф'

    # main_buttons = [InlineKeyboardButton(text=op_str, callback_data='switchop'),
    #                InlineKeyboardButton(text=ref_str, callback_data='switchref')]
    keyboard.add(InlineKeyboardButton(text=op_str, callback_data='switchop'))
    keyboard.add(InlineKeyboardButton(text=ref_str, callback_data='switchref'))
    keyboard.add(InlineKeyboardButton(text='Проверка каналов', callback_data='check_channels_admin'))
    keyboard.add(InlineKeyboardButton(text='◀️ Вернуться', callback_data='back'))
    keyboard.adjust(1).row()
    return keyboard.as_markup()


async def have_to_sub(user, bot):
    keyboard = InlineKeyboardBuilder()

    ## Step 1: Check bot admin channels in enabled op btns and deactivate
    answer = await check_admin_channels(bot)

    ## Step 2: Get links of actual btns
    actual_ops = await get_actual_op_full()

    ## Step 2.2 - Check user in channel
    need_to_sub = []
    for op in actual_ops:
        link = str(op.op_username)
        channel = await check_user_subs(user, bot, link)
        if channel:
            need_to_sub.append(channel)
            print(f'Не подписан на канал: {channel}')
        if not channel:
            print(f'Пользователь подписан на канал: {channel}')

    ## Step 3: Msg 'Вам необходимо подписаться на эти каналы для продолжения'

    for channelnick in need_to_sub:
        username = str(channelnick)
        name = await get_name_by_username(username)
        link = await get_link_by_username(username)
        keyboard.add(InlineKeyboardButton(text=name, url=link))

    ## Step 4: Check after 1-2 min after this msg and count if OK

    ## Ввообще это все в utils бы перенести, а не в билдер клавиатуры

    # Coroutine.start(1-2min) И сравнить два списка старый и новый по тому же принципу и разницу посчитать и добавить оп

    ## Step 5:

    keyboard.adjust(2).row()
    return keyboard.as_markup()
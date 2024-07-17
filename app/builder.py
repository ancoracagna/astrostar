from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
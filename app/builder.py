from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def ref_code_key(ref_code):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=ref_code, callback_data=f'refcode_{ref_code}'))
    return keyboard.adjust(1).as_markup()
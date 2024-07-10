from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

adminpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='📊 Статистика', callback_data= 'stat')],
                                   [InlineKeyboardButton(text='📤 Рассылка', callback_data= 'sendall')],
                                   [InlineKeyboardButton(text='👥 Пользователи', callback_data='users')],
                                   [InlineKeyboardButton(text='💸 Маркетинг', callback_data='marketing')]])

apanelback = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='◀️ Вернуться', callback_data='back')]])

marketpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔗 Создать ссылку', callback_data= 'create_ref_code')],
                                                    [InlineKeyboardButton(text='📋 Список ссылок', callback_data= 'ref_code_lst')],
                                                    [InlineKeyboardButton(text='✏️ Ввести вручную', callback_data= 'manual_ref_search')]])

apanelsendall = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🖼 С картинкой', callback_data='sendallpic')],
                                                      [InlineKeyboardButton(text='✏️ Без картинки', callback_data='sendalltxt')],
                                                      [InlineKeyboardButton(text='◀️ Вернуться', callback_data='back')]])

createbtn_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data='create_btn')],
                                                     [InlineKeyboardButton(text='Нет',callback_data='continue_withoutbtn')]])

#Сделать генератор кнопки и счетчик на ней

userpanel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='👩‍❤️‍👨 Проверить совместимость'), KeyboardButton(text='🔮 Гороскоп')],
                                          [KeyboardButton(text='🪐 Профиль'), KeyboardButton(text='✏️ Поддержка')]], resize_keyboard=True)

comp_panel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отменить проверку')]], resize_keyboard=True)

async def result(tg_id, desc):
    resultpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='💫 Узнать результат!', callback_data=f'result_{tg_id}_{desc}')]])
    return resultpanel
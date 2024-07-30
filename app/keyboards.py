from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

adminpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='📊 Статистика', callback_data= 'stat')],
                                   [InlineKeyboardButton(text='📤 Рассылка', callback_data= 'sendall')],
                                   [InlineKeyboardButton(text='👥 Пользователи', callback_data='users')],
                                   [InlineKeyboardButton(text='💸 Маркетинг', callback_data='marketing')],
                                   [InlineKeyboardButton(text='🛠 Глобальные настройки', callback_data='admin_settings')]])


apanelback = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='◀️ Вернуться', callback_data='back')]])

mpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Реферальные ссылки', callback_data='refs_menu')],
                                               [InlineKeyboardButton(text='ОП', callback_data='op_menu')]])

marketpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔗 Создать ссылку', callback_data= 'create_ref_code')],
                                                    [InlineKeyboardButton(text='📋 Список ссылок', callback_data= 'ref_code_lst')],
                                                    [InlineKeyboardButton(text='✏️ Ввести вручную', callback_data= 'manual_ref_search')]])

op_panel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Создать ОП кнопку', callback_data='create_op')],
                                                 [InlineKeyboardButton(text='Список ОП кнопок', callback_data='oplist')],
                                                 [InlineKeyboardButton(text='◀️ Вернуться', callback_data='back')]])

apanelsendall = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🖼 С картинкой', callback_data='sendallpic')],
                                                      [InlineKeyboardButton(text='✏️ Без картинки', callback_data='sendalltxt')],
                                                      [InlineKeyboardButton(text='📝 По шаблону', callback_data='sendtemplate')],
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

templatesend = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data= 'confirm_send')],
                                                     [InlineKeyboardButton(text='Нет', callback_data= 'canceltemplate')]])

zodiakkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♈ Овен', callback_data='zodiak_aries'), InlineKeyboardButton(text='♉ Телец', callback_data='zodiak_taurus')],
    [InlineKeyboardButton(text='♊ Близнецы', callback_data='zodiak_gemini'), InlineKeyboardButton(text='♋ Рак', callback_data='zodiak_cancer')],
    [InlineKeyboardButton(text='♌ Лев', callback_data='zodiak_leo'), InlineKeyboardButton(text='♍ Дева', callback_data='zodiak_virgo')],
    [InlineKeyboardButton(text='♎ Весы', callback_data='zodiak_libra'), InlineKeyboardButton(text='♏ Скорпион', callback_data='zodiak_scorpio')],
    [InlineKeyboardButton(text='♐ Стрелец', callback_data='zodiak_sagittarius'), InlineKeyboardButton(text='♑ Козерог', callback_data='zodiak_capricorn')],
    [InlineKeyboardButton(text='♒ Водолей', callback_data='zodiak_aquarius'), InlineKeyboardButton(text='♓ Рыбы', callback_data='zodiak_pisces')]
])

op_create_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data='createopbtn')],
                                                     [InlineKeyboardButton(text='Нет', callback_data='cancelopbtn')]])
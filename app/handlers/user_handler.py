from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.requests import (set_user, get_refs, get_user_data, add_ref, add_check, get_check, get_horoscope, reg_event,
                             add_ref_event)
from app.keyboards import userpanel, comp_panel, result
from app.states import Compatibility
from app.utils.utils import get_refer_id, gen_res, gen_unique
from app.filters.main_filter import ADMINS as admins

router = Router()

universe_text = ('Чтоб получить информацию о своем профиле воспользуйся кнопкой "Профиль" или специальной '
                 'командой из командного меню.')

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    user_info = await get_user_data(message.from_user.id)
    if user_info:
        response_text = f'{message.from_user.full_name}, Вижу что вы уже в моей базе данных. Приятного пользования ботом! 🥰'
        await message.answer(text=response_text, reply_markup=userpanel)
        refer_id = get_refer_id(command.args)
        if refer_id:
            await add_ref_event(message.from_user.id, 'olduserstart', refer_id)
        else:
            refer_id = 0
            await add_ref_event(message.from_user.id, 'olduserstart', refer_id)
    else:
        refer_id = get_refer_id(command.args)
        print(f'ref: {refer_id}')
        if refer_id:
            await message.answer('✨ Приветствуем вас! ✨\n\n'
                                 'Добро пожаловать в наш уникальный проект, где мы помогаем вам узнать, насколько вы совместимы с другими людьми, и составляем гороскопы. 🔮💫\n\n'
                                 'Наш бот готов предложить вам удивительное сочетание астрологических прогнозов и анализа совместимости, чтобы сделать вашу жизнь ярче и интереснее. 🌟👫\n\n'
                                 'Перейдите в желаемый раздел и узнайте % совместимости прямо сейчас! 🚀🔭\n\n'
                                 f'Ваши звезды ждут! 🌠🌌 Пользователю: {refer_id} капнула звездочка за вас! ⭐️',
                                 reply_markup=userpanel)
            await add_ref_event(message.from_user.id, 'newuser', refer_id)
        else:
            await message.answer('✨ Приветствуем вас! ✨\n\n'
                                 'Добро пожаловать в наш уникальный проект, где мы помогаем вам узнать, насколько вы совместимы с другими людьми, и составляем гороскопы. 🔮💫\n\n'
                                 'Наш бот готов предложить вам удивительное сочетание астрологических прогнозов и анализа совместимости, чтобы сделать вашу жизнь ярче и интереснее. 🌟👫\n\n'
                                 'Перейдите в желаемый раздел и узнайте % совместимости прямо сейчас!! 🚀🔭\n\n'
                                 f'Ваши звезды ждут! 🌠🌌️',
                                 reply_markup=userpanel)
            refer_id = 0
            await add_ref_event(message.from_user.id, 'newuser', refer_id)
        await set_user(message.from_user.id, refer_id)
        try:
            await add_ref(refer_id)
        except:
            print('Не удалось добавить реф')
        for admin in admins:
            await bot.send_message(admin, 'У нас новый пользователь')
        try:
            await bot.send_sticker(refer_id,sticker=r'CAACAgIAAxkBAAEMcYRmiNpqfM5y7VhKNlm3ycmr23d0xQACn04AAvaYQEtotJWy5QHbAjUE')
            await bot.send_message(refer_id, text='*Поздравляем\!* 🥳\nУ вас новая звездочка ⭐',parse_mode=ParseMode.MARKDOWN_V2)
        except:
            print('Пользователь не найден')


@router.message(F.text == 'Отменить проверку')
async def compatibility(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы вернулись в главное меню!', reply_markup= userpanel)

@router.message(F.text == '✏️ Поддержка')
async def help(message: Message):
    await message.answer('По всем вопросам - @genesisup')

@router.message(F.text == '👩‍❤️‍👨 Проверить совместимость')
async def compatibility(message: Message, state: FSMContext):
    await state.set_state(Compatibility.firstinfo)
    await reg_event('Совместимость')
    await message.answer('_Пример результата_\n_Повторные генерации одних и тех же людей могу давать искаженный результат_',parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer_photo(photo=FSInputFile('example.png'), caption=''
                         '*Шаг 1: Информация о первом человеке*\n'
                         'Пожалуйста, введите следующую информацию:\n\n'
                         'Имя: ✏️\n'
                         'Возраст: 📅\n'
                         'Пол: 👤\n'
                         'Знак зодиака: ♈♉♊♋♌♍♎♏♐♑♒♓\n\n'
                         'Пример: `Виктор 21 М Весы` или `Снежана 16 Д ♐`', parse_mode=ParseMode.MARKDOWN_V2, reply_markup=comp_panel)

@router.message(Compatibility.firstinfo)
async def compatibility_2(message: Message, state: FSMContext):
    await state.update_data(firstinfo=message.text)
    await state.set_state(Compatibility.firstimg)
    await message.answer('*Шаг 2: Пожалуйста, загрузите фотографию первого человека* 📸',parse_mode=ParseMode.MARKDOWN_V2)

@router.message(Compatibility.firstimg)
async def compatibility_3(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(firstimg=message.photo[-1].file_id)
        await state.set_state(Compatibility.secondinfo)
        await message.answer('*Шаг 3: Информация о втором человеке*\n'
                             'Пожалуйста, введите следующую информацию:\n\n'
                             'Имя: ✏️\n'
                             'Возраст: 📅\n'
                             'Пол: 👤\n'
                             'Знак зодиака: ♈♉♊♋♌♍♎♏♐♑♒♓\n\n'
                             'Пример: `Виктор 21 М Весы` или `Снежана 16 Д ♐`',parse_mode=ParseMode.MARKDOWN_V2, reply_markup=comp_panel)
    else:
        await message.answer('Вы отправили не фотографию, попробуйте еще раз или отмените проверку и вернитесь в меню')


@router.message(Compatibility.secondinfo)
async def compatibility_4(message: Message, state: FSMContext):
    await state.update_data(secondinfo=message.text)
    await message.answer('*Шаг 4: Пожалуйста, загрузите фотографию второго человека* 📸',parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Compatibility.result)



@router.message(Compatibility.result)
async def compatibility_last(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(secondimg=message.photo[-1].file_id)
        data = await state.get_data()
        desc = str(data["firstinfo"]) + "_" + str(data["secondinfo"])
        unique = gen_unique()
        await message.answer_photo(photo=FSInputFile('result.png'),
                                   caption=f'Информация о {data["firstinfo"]} и '
                                   f'{data["secondinfo"]}', reply_markup= await result(message.from_user.id, unique))
        res = gen_res()
        await add_check(message.from_user.id, desc, res, unique)

        await state.clear()
    else:
        await message.answer('Вы отправили не фотографию, попробуйте еще раз или отмените проверку и вернитесь в меню')

@router.message(F.text=='🪐 Профиль')
async def profile(message: Message):
    refs = await get_refs(message.from_user.id)
    link = 'https://t.me/astrostar_bot?start='+str(message.from_user.id)
    await message.answer(f'👤 Пользователь: {message.from_user.full_name}\n⭐️ Кол-во звездочек: {refs}\n🔗 Ваша ссылка для привлечения: {link}')

@router.message(F.text == '🔮 Гороскоп')
async def horoscope(message: Message):
    forecast = await get_horoscope()
    await reg_event('Гороскоп')
    await message.answer(f'Гороскоп на сегодня:\n\n{forecast}',parse_mode=ParseMode.MARKDOWN_V2)

@router.callback_query(F.data.startswith('result_'))
async def get_result(callback: CallbackQuery):
    await callback.answer('Успешно!')
    data = callback.data.split('_')
    refs = await get_refs(data[1])
    count = 3-refs
    link = 'https://t.me/astrostar_bot?start=' + str(data[1])
    if count >0:
        await callback.message.answer(f'Для того чтобы узнать результат пригласите еще {count} пользователя\n\nТекущее количество: {refs} ⭐️\n\nВаша ссылка: {link}', reply_markup=userpanel)
    else:
        msg = await get_check(data[2])
        await callback.message.answer(f'{msg}',parse_mode=ParseMode.MARKDOWN_V2, reply_markup=userpanel)
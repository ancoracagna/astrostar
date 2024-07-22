from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from app.db.requests import reg_event, add_check
from app.keyboards import comp_panel, result, zodiakkb
from app.states import Compatibility
from app.utils.utils import gen_unique, gen_res

router = Router()
@router.message(F.text == '👩‍❤️‍👨 Проверить совместимость')
async def compatibility(message: Message, state: FSMContext):
    await state.set_state(Compatibility.firstinfo)
    await message.answer('_Пример результата_\n_Повторные генерации одних и тех же людей могут давать искаженный результат_', parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer_photo(photo=FSInputFile('example.png'), caption=
                               '*Шаг 1: Информация о парне*\n'
                               'Пожалуйста, введите следующую информацию:\n\n'
                               'Имя: ✏️\n'
                               'Возраст: 📅\n'
                               'Пример: `Александр 16`', parse_mode=ParseMode.MARKDOWN_V2)

@router.message(Compatibility.firstinfo)
async def compatibility_2(message: Message, state: FSMContext):
    await state.update_data(firstinfo=message.text)
    await state.set_state(Compatibility.firstzodiak)
    await message.answer('*Шаг 2: Пожалуйста, выберите знак зодиака парня* 📸', parse_mode=ParseMode.MARKDOWN_V2, reply_markup=zodiakkb)

@router.callback_query(F.data.startswith('zodiak_'), Compatibility.firstzodiak)
async def select_first_zodiak(callback: CallbackQuery, state: FSMContext):
    await state.update_data(firstzodiak=callback.data)
    await state.set_state(Compatibility.secondinfo)
    await callback.message.answer('*Шаг 3: Информация о девушке*\n'
                                  'Пожалуйста, введите следующую информацию:\n\n'
                                  'Имя: ✏️\n'
                                  'Возраст: 📅\n'
                                  'Пример: `Алина 15`', parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer()

@router.message(Compatibility.secondinfo)
async def compatibility_4(message: Message, state: FSMContext):
    await state.update_data(secondinfo=message.text)
    await state.set_state(Compatibility.secondzodiak)
    await message.answer('*Шаг 4: Пожалуйста, выберите знак зодиака девушки* 📸', parse_mode=ParseMode.MARKDOWN_V2, reply_markup=zodiakkb)

@router.callback_query(F.data.startswith('zodiak_'), Compatibility.secondzodiak)
async def select_second_zodiak(callback: CallbackQuery, state: FSMContext):
    await state.update_data(secondzodiak=callback.data)
    data = await state.get_data()
    desc = str(data["firstinfo"]) + "_" + str(data["secondinfo"])
    unique = gen_unique()
    await callback.message.answer_photo(photo=FSInputFile('result.png'),
                               caption=f'Информация о {data["firstinfo"]} и '
                                       f'{data["secondinfo"]}', reply_markup=await result(callback.from_user.id, unique))
    res = gen_res()
    await add_check(callback.from_user.id, desc, res, unique)

    await state.clear()

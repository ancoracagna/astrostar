from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Compatibility(StatesGroup):
    firstinfo = State()
    firstzodiak = State()
    secondinfo = State()
    secondzodiak = State()
    result = State()

class SendAllPic(StatesGroup):
    img = State()
    text = State()

class SendAllText(StatesGroup):
    text = State()

class Marketing(StatesGroup):
    ref_name = State()

class New_Ref(StatesGroup):
    price = State()
    ref_name = State()

class BroadcastState(StatesGroup):
    waiting_for_message = State()
    confirm_message = State()

class OP_State(StatesGroup):
    link = State()
    name = State()
    username = State()
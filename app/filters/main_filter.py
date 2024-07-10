from aiogram import types
from aiogram.filters import Filter

ADMINS = [408531138]

class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins
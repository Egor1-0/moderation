from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command


generator_link = Router()


@generator_link.message(Command('add_traffic'))
async def add_chennals_traffic(message: Message):
    await message.answer('Введите id на канал')
    

@generator_link.callback_query(F.data == '')
async def generate_link(call: CallbackQuery):
    
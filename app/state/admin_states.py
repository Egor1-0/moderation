from aiogram.fsm.state import State, StatesGroup


class AddingFunctions(StatesGroup):
    add_channel_id = State()
    add_channel_link = State()
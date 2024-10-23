from aiogram.fsm.state import State, StatesGroup


class BuySponsor(StatesGroup):
    get_count = State()
    get_id = State()
    get_link = State()
    
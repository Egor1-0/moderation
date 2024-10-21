from aiogram.fsm.state import State, StatesGroup


class BuySponsor(StatesGroup):
    get_count = State()
    get_link = State()
    # cont = State()
from aiogram.fsm.state import State, StatesGroup


class AddChannel(StatesGroup):
    add_channel_id = State()
    add_channel_link = State()


class FindUser(StatesGroup):
    find_user = State()
    amount_money = State()


class MassSend(StatesGroup):
    get_mes = State()


class AddAdmin(StatesGroup):
    add_admin_id = State()


class UpdatePrice(StatesGroup):
    name_price = State()
    price = State()


from aiogram.fsm.state import State, StatesGroup


class AddChannel(StatesGroup):
    add_channel_id = State()
    add_channel_link = State()


class FindUser(StatesGroup):
    find_user = State()
    amount_money = State()
    text_send = State()
    subscription = State()


class MassSend(StatesGroup):
    get_mes = State()


class AddAdmin(StatesGroup):
    add_admin_id = State()


class UpdatePrice(StatesGroup):
    name_price = State()
    price = State()

class AddAccount(StatesGroup):
    phone = State()
    code = State()
    phone_code_hash = State()
    password = State()
    
    
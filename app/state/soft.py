from aiogram.fsm.state import State, StatesGroup


class AddBase(StatesGroup):
    name_base = State()
    chat_link = State()
    

class CreateTask(StatesGroup):
    name_task = State()
    name_base = State()
    text_sms = State()
    interval_sms = State()
    flow = State()
    

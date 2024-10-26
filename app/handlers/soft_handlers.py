import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.queries import (get_my_account, get_user, save_session, 
                                  save_chat_base, get_my_bases, add_tastk)
from app.state.soft import AddBase, CreateTask

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboard.soft_kb import soft_menu, generate_account_kb, soft_start

from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError
from app.state.admin_states import AddAccount
from opentele.tl import TelegramClient
from opentele.api import API


soft_handler = Router()

def create_client(session_name: str) -> TelegramClient:
    """Создаёт клиента сессии с именем '{номер}.session'."""
    return TelegramClient(
        session_name,
        API.TelegramDesktop.Generate(unique_id=session_name)
    )


def sanitize_session_name(raw_name: str) -> str:
    """Удаляет пробелы и неалфавитные символы из имени сессии."""
    return re.sub(r'\W+', '', raw_name)


@soft_handler.callback_query(F.data == 'soft_panels')
@soft_handler.callback_query(F.data == 'back_profile_acc')
async def my_soft(call: CallbackQuery):
    await call.message.edit_caption(caption=(
      f"<b>🖥 Traffic менеджер V1 - софт \n\n</b>"
      f"<b>📡 Информация: \n</b>"
      f"<b>┣Подписка :</b>\n"
      f"<b>┣Задач активных:</b> \n"  
      f"<b>┣Всего сообщение рассылано:</b> \n"
      f"<b>┗Чатов: </b>\n\n"
      f"<b>❗️ Не используйте основные аккаунты </b>"
    ), reply_markup=soft_menu)
    
    
    
@soft_handler.callback_query(F.data == 'my_accounts')
async def my_account(call: CallbackQuery):
    # Получаем аккаунты, если None - возвращаем пустой список
    accounts = await get_my_account(call.message.from_user.id) or []
    account_count = len(accounts)  # Количество аккаунтов

    # Ожидаем выполнения функции get_user
    subscrib = await get_user(call.message.from_user.id)  # Добавлено await здесь
    subscription_info = subscrib.subscription if subscrib else "❌ не подключен  "

    # Генерируем клавиатуру
    keyboard = generate_account_kb(account_count)

    # Редактируем сообщение с новыми данными
    await call.message.edit_caption(
        caption=(
            f"<b>🖥 Traffic менеджер V1 - софт </b>\n\n"
            f"<b>💻 Информация: </b>\n"
            f"<b>┣🆔 Мой ID: </b> <code>{call.from_user.id}</code> \n"
            f"<b>┣📱 Номер: </b> <code>{account_count}</code>\n"
            f"<b>┗📅Подписка: </b> <code>{subscription_info}</code> \n"
        ),
        reply_markup=keyboard
    )

@soft_handler.callback_query(F.data == 'add_account')
async def add_user_account(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddAccount.phone)
    await call.message.answer('<b>📲 Введите номер телефона </b>')
    

@soft_handler.message(AddAccount.phone)
async def add_phone(message: Message, state: FSMContext):
    phone_number = message.text.strip()
    await state.update_data(phone=message.text)

    session_name = sanitize_session_name(f"{phone_number}")
    client = create_client(session_name)
    
    await client.connect()
    
    try:
        send_code = await client.send_code_request(phone_number)
        await state.update_data(phone_code_hash=send_code.phone_code_hash)
        await state.set_state(AddAccount.code)
            
        await save_session(message.from_user.id, session_name, phone_number)
        
        
        await message.answer('<b>📩 Введите СМС </b>')
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

        
        
@soft_handler.message(AddAccount.code)
async def add_code(message: Message, state: FSMContext):
    account = await state.get_data()
    code = message.text.strip()
    phone = account['phone']
    
    user = await get_my_account(message.from_user.id)
    
    client = create_client(user.session_name)
    await client.connect()
    
    phone_code_hash = account.get('phone_code_hash')
    
    try:
        await client.sign_in(
            phone=phone, 
            code=code, 
            phone_code_hash=phone_code_hash
        )
        await message.answer('<b>✅ Аккаунт успешно добавлен</b>')
        await state.clear()
    except SessionPasswordNeededError:
        await message.answer('<b>🔐 Введите пороль от 2FA</b>')
        await state.set_state(AddAccount.password)
        

@soft_handler.message(AddAccount.password)
async def add_password(message: Message, state: FSMContext):
    password = message.text
    
    user = await get_my_account(message.from_user.id)
    client = create_client(user.session_name)
    
    await client.connect()
    
    try:
        await client.sign_in(password=password)
        await message.answer('<i>✅ Аккаунт успешно добавлен</i>')
        await state.clear()
    except PasswordHashInvalidError:
        await message.answer('❌ Неправильный пароль. Попробуйте снова.')
        await state.set_state(AddAccount.password)

    

@soft_handler.callback_query(F.data == 'my_base')
async def add_base(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddBase.name_base)
    await call.message.answer('<b>✏️ Введите название базы</b>')
    

@soft_handler.message(AddBase.name_base)
async def add_my_base(message: Message, state: FSMContext):
    await state.update_data(name_base=message.text)
    await state.set_state(AddBase.chat_link)
    
    await message.answer('<b>📖 Пришлите базу чатов каждую через новую строку </b>')
    
    
@soft_handler.message(AddBase.chat_link)
async def add_chat_link(message: Message, state: FSMContext):
    await state.update_data(chat_link=message.text)
    data = await state.get_data()
    name_base = data.get('name_base')
    
    chat_links = message.text.splitlines()
    
    for link in chat_links:
        # Сохраняем каждую ссылку как отдельную базу чатов
        await save_chat_base(message.from_user.id, name_base, link.strip())
        
    await message.answer('<b>✅ Базы чатов успешно добавлены!</b>')
    await state.clear() 
    
    
# Рассылка 

@soft_handler.callback_query(F.data == 'create_task')
async def add_task(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreateTask.name_task)
    await call.message.answer('<b>✏️ Введите название задачи</b>')
    
    

def create_inline_keyboard(bases: list):
    keyboard = InlineKeyboardBuilder()
    # Создаем кнопку для каждого уникального названия базы
    unique_bases = {base.name_base for base in bases}  # Уникальные названия
    for name in unique_bases:
        button = InlineKeyboardButton(text=name, callback_data=f"select_base_{name}")
        keyboard.add(button)
    return keyboard.adjust(1).as_markup()


@soft_handler.message(CreateTask.name_task)
async def add_name_task(message: Message, state: FSMContext):
    await state.update_data(name_task=message.text)
    await state.set_state(CreateTask.name_base)

    # Получаем уникальные базы для пользователя
    bases = await get_my_bases(message.from_user.id)
    # Создаем инлайн-клавиатуру с кнопками
    keyboard = create_inline_keyboard(bases)

    # Отправляем сообщение с клавиатурой
    await message.answer("Выберите базу:", reply_markup=keyboard)
    
    
@soft_handler.callback_query(CreateTask.name_base)
async def add_bases(call: CallbackQuery, state: FSMContext):
    await state.update_data(name_base=call.data.split('_')[2])
    await state.set_state(CreateTask.interval_sms)
    
    await call.message.answer('<b>⏰ Введите интервал между потоками </b>')
    

@soft_handler.message(CreateTask.interval_sms)
async def add_interval(message: Message, state: FSMContext):
   await state.update_data(interval_sms=message.text)
   await state.set_state(CreateTask.text_sms)
   
   await message.answer('<b>📤 Пришлите ваш текст </b>')


@soft_handler.message(CreateTask.text_sms)
async def add_text_sms(message: Message, state: FSMContext):
    await state.update_data(text_sms=message.text)
    await state.set_state(CreateTask.flow)
    
    await message.answer('<b>🔁 Введите количество потоков </b>')
    

@soft_handler.message(CreateTask.flow)
async def add_flow(message: Message, state: FSMContext):
    await state.update_data(flow=message.text)
    data = await state.get_data()
    
    await add_tastk(message.from_user.id, data['name_task'], data['name_base'], data['text_sms'], data['flow'], data['interval_sms'],)
    
    await state.clear()
    
    await message.answer('<b>⚙️ Настройки сохранены </b>', reply_markup=soft_start)
    
    

    
import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.queries import get_my_account, get_user, save_session

from app.keyboard.soft_kb import soft_menu
from app.keyboard.soft_kb import generate_account_kb


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

    

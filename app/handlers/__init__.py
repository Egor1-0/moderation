from aiogram import Router
from app.handlers.start_handlers import start_handler
from app.handlers.user_profile import user_profile

handlers_ = Router()

handlers_.include_routers(start_handler, user_profile)
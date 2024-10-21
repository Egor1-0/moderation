from aiogram import Router

from app.handlers.start_handlers import start_handler
from app.handlers.user_profile import user_profile
from app.handlers.admin.admin_handlers import admin_router
from app.handlers.shop import shop_router

handlers_ = Router()

handlers_.include_routers(start_handler, user_profile, admin_router, shop_router)
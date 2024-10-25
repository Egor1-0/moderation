from aiogram import Router

from app.handlers.menu_handlers import menu_handler
from app.handlers.user_profile import user_profile
from app.handlers.admin.admin_handlers import admin_router
from app.handlers.shop import shop_router
from app.handlers.soft_handlers import soft_handler
from app.middlewares.check_subscription import CheckSubscription

handlers_ = Router()

handlers_.include_routers(menu_handler, user_profile, admin_router, shop_router, soft_handler)


    
handlers_.message.middleware(CheckSubscription())
handlers_.callback_query.middleware(CheckSubscription())

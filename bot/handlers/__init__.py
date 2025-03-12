from aiogram import Router
from .start import router as start_router
from bot.handlers.callbacks.start_callback import router as callback_router
from bot.handlers.admin_handlers.users import router as users_router
from .subscribes import router as subscribes_router
from .callbacks.subscribes_callback import router as callback_sub_router
from .admin_handlers.id import router as cmd_id_router
from .callbacks.id_callback import router as callback_id_router

router = Router()
router.include_router(start_router)
router.include_router(callback_router)
router.include_router(users_router)
router.include_router(subscribes_router)
router.include_router(callback_sub_router)
router.include_router(cmd_id_router)
router.include_router(callback_id_router)
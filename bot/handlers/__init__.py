from aiogram import Router
from .start import router as start_router
from bot.handlers.callbacks.callback import router as callback_router

router = Router()
router.include_router(start_router)
router.include_router(callback_router)

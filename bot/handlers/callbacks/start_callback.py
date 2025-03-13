from aiogram import Router, types
from aiogram.filters import Command
from database import update_user_status, get_user

router = Router()

@router.callback_query(lambda c: c.data.startswith("approve_"))
async def approve_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    await update_user_status(user_id, "approved")

    user = await get_user(user_id)

    if user:
        await callback.message.edit_text(f"Пользователь {user[2]} {user[3]} @{user[4]} был одобрен.")
        await callback.bot.send_message(user_id, "Запрос одобрен. Команда /subscribes позволит подписаться на обновления")
    else:
        await callback.message.edit_text(f"Пользователь не найден")

@router.callback_query(lambda c: c.data.startswith("reject_"))
async def reject_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    await update_user_status(user_id, "rejected")

    user = await get_user(user_id)
    if user:
        await callback.message.edit_text(f"Пользователь {user[2]} {user[3]} @{user[4]} был отклонен.")
        await callback.bot.send_message(user_id, "Ваш запрос на доступ отклонен")
    else:
        await callback.message.edit_text(f"Пользователь не найден")

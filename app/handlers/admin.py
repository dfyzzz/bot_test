from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.database.models import User
from app.dialogs.admin_dialog import AdminSG

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message, session, dialog_manager: DialogManager):
    """Admin command handler - launches admin panel dialog"""
    if message.from_user is None:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    # Check if user is admin
    from sqlalchemy import select
    result = await session.execute(select(User).filter(User.telegram_id == message.from_user.id))
    user = result.scalar_one_or_none()
    if not user or not user.is_admin:
        await message.answer("У вас нет прав администратора")
        return

    # Launch admin panel dialog
    await dialog_manager.start(AdminSG.main, mode=StartMode.RESET_STACK)

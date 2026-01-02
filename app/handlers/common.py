from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.database.models import User
from app.dialogs.main_menu import MainMenuSG

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, session, dialog_manager: DialogManager):
    """Start command handler - launches main menu dialog"""
    # Check if user exists in database
    if message.from_user is None:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return
    
    # Use existing database functions instead of direct SQLAlchemy calls
    from app.database.requests import get_or_create_user
    user = await get_or_create_user(session, message.from_user.id, message.from_user.first_name, message.from_user.username)
    
    if not user:
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")
        return
    
    # Start the main menu dialog instead of sending a message
    is_admin = user.is_admin if user else False
    # Pass the admin status to the dialog data
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)

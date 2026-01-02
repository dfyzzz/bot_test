from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.dialogs.profile_dialog import ProfileSG

router = Router()


@router.message(Command("profile"))
async def profile_command(message: Message, dialog_manager: DialogManager):
    """User profile command handler - launches profile dialog"""
    await dialog_manager.start(ProfileSG.show_profile, mode=StartMode.RESET_STACK)


@router.message(Command("history"))
async def history_command(message: Message, dialog_manager: DialogManager):
    """History command handler - launches history dialog"""
    await dialog_manager.start(ProfileSG.show_history, mode=StartMode.RESET_STACK)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from app.dialogs.booking_dialog import BookingSG

router = Router()


@router.message(Command("book"))
async def book_command(message: Message, dialog_manager: DialogManager):
    """Booking command handler - launches booking dialog"""
    await dialog_manager.start(BookingSG.choose_service, mode=StartMode.RESET_STACK)

from aiogram import Router
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Start, Row
from aiogram_dialog.widgets.text import Format, Const

from app.dialogs.booking_dialog import BookingSG
from app.dialogs.profile_dialog import ProfileSG

router = Router()


# States for main menu
from aiogram.fsm.state import State, StatesGroup

class MainMenuSG(StatesGroup):
    main = State()


# Data getter for main menu
async def main_menu_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем сессию из данных middleware
    session = kwargs.get("session")
    event = kwargs.get("event")
    if event and hasattr(event, 'from_user') and event.from_user:
        user_id = event.from_user.id
    else:
        # Если не можем получить ID пользователя, возвращаем заглушку
        return {
            "is_admin": False,
            "show_admin_panel": False
        }

    is_admin = False
    if session:
        from app.utils.db_helpers import get_user_by_telegram_id
        user = await get_user_by_telegram_id(session, user_id)
        is_admin = user.is_admin if user and hasattr(user, 'is_admin') else False

    return {
        "is_admin": is_admin,
        "show_admin_panel": is_admin
    }


# Main menu dialog for non-admins
main_menu_dialog = Dialog(
    Window(
        Format("🤖 Главное меню\n\nВыберите действие:"),
        Column(
            Start(Format("📅 Записаться"), id="book", state=BookingSG.choose_service),
            Start(Format("👤 Личный кабинет"), id="profile", state=ProfileSG.show_profile),
            Button(Format("📞 Контакты"), id="contacts"),
            Button(Format("⭐ Оставить отзыв"), id="feedback"),
        ),
        state=MainMenuSG.main,
        getter=main_menu_getter,
    ),
)
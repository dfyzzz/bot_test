from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const

from app.database.models import User, Booking
from sqlalchemy import select

router = Router()

# States for profile dialog
from aiogram.fsm.state import State, StatesGroup

class ProfileSG(StatesGroup):
    show_profile = State()
    show_history = State()
    edit_profile = State()


# Data getter for profile
async def profile_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем сессию из данных middleware
    session = kwargs.get("session")
    event = kwargs.get("event")
    if event and hasattr(event, 'from_user') and event.from_user:
        user_id = event.from_user.id
        first_name = getattr(event.from_user, 'first_name', None)
        username = getattr(event.from_user, 'username', None)
    else:
        # Если не можем получить ID пользователя, возвращаем заглушку
        return {
            "user_name": "Иван Иванов",
            "user_phone": "+7 (999) 999-99-99",
            "booking_count": 0,
            "loyalty_points": 0
        }

    if session:
        # Используем существующую функцию для получения пользователя
        from app.database.requests import get_or_create_user
        user = await get_or_create_user(session, user_id, first_name, username)
        if user:
            # Получаем записи пользователя
            booking_result = await session.execute(
                select(Booking).where(Booking.user_id == user.id).order_by(Booking.created_at.desc())
            )
            bookings = booking_result.scalars().all()
            
            return {
                "user_name": user.name,
                "user_phone": user.phone or "Не указан",
                "booking_count": len(bookings),
                "loyalty_points": getattr(user, 'loyalty_points', 0) or 0
            }

    # Возврат заглушки, если сессия недоступна или пользователь не найден
    return {
        "user_name": "Иван Иванов",
        "user_phone": "+7 (999) 999-99-99",
        "booking_count": 0,
        "loyalty_points": 0
    }


# Data getter for history
async def history_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем сессию из данных middleware
    session = kwargs.get("session")
    event = kwargs.get("event")
    if event and hasattr(event, 'from_user') and event.from_user:
        user_id = event.from_user.id
        first_name = getattr(event.from_user, 'first_name', None)
        username = getattr(event.from_user, 'username', None)
    else:
        # Если не можем получить ID пользователя, возвращаем заглушку
        return {
            "total_bookings": 0,
            "booking_lines_str": "У вас пока нет записей"
        }

    if session:
        # Используем существующую функцию для получения пользователя
        from app.database.requests import get_or_create_user
        user = await get_or_create_user(session, user_id, first_name, username)
        if user:
            # Получаем записи пользователя
            booking_result = await session.execute(
                select(Booking).where(Booking.user_id == user.id).order_by(Booking.created_at.desc())
            )
            bookings = booking_result.scalars().all()
            
            # Формируем строки истории записей
            booking_lines = []
            for booking in bookings[:10]:  # Показываем последние 10 записей
                service_name = booking.service.name if booking.service else "Не указана"
                booking_lines.append(
                    f"• {booking.date.strftime('%d.%m.%Y')} в {booking.time.strftime('%H:%M')} ({service_name})"
                )
            
            return {
                "total_bookings": len(bookings),
                "booking_lines_str": "\n".join(booking_lines) if booking_lines else "У вас пока нет записей"
            }

    # Возврат заглушки, если сессия недоступна или пользователь не найден
    return {
        "total_bookings": 0,
        "booking_lines_str": "У вас пока нет записей"
    }


# Callback function to show history
async def show_history(callback: CallbackQuery, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(ProfileSG.show_history)


# Callback function to return to profile
async def back_to_profile(callback: CallbackQuery, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(ProfileSG.show_profile)


# Profile dialog
profile_dialog = Dialog(
    Window(
        Format("👤 Ваш профиль\n\n"
               "Имя: {user_name}\n"
               "Телефон: {user_phone}\n"
               "Количество записей: {booking_count}\n"
               "Баллы лояльности: {loyalty_points}%"),
        Row(
            Button(Const("✏️ Редактировать"), id="edit_profile"),
            Button(Const("📋 История записей"), id="show_history_btn", on_click=show_history),
        ),
        Cancel(Const("◀️ Назад")),
        state=ProfileSG.show_profile,
        getter=profile_getter,
    ),
    Window(
        Format("📋 История ваших записей\n\n"
               "Всего записей: {total_bookings}\n\n"
               "{booking_lines_str}"),
        Button(Const("🔙 Назад к профилю"), id="back_to_profile", on_click=back_to_profile),
        state=ProfileSG.show_history,
        getter=history_getter
    ),
)
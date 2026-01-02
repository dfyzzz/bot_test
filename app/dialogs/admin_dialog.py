from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const

from app.database.models import User, Booking, Service
from sqlalchemy import select

router = Router()

# States for admin dialog
from aiogram.fsm.state import State, StatesGroup

class AdminSG(StatesGroup):
    main = State()
    show_bookings = State()
    show_clients = State()
    show_stats = State()
    broadcast = State()


# Data getter for admin panel
async def admin_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем сессию из данных события
    session = kwargs.get("session")
    event = kwargs.get("event")
    if event and hasattr(event, 'from_user') and event.from_user:
        user_id = event.from_user.id
    else:
        # Если не можем получить ID пользователя, возвращаем заглушку
        return {
            "total_clients": 0,
            "today_bookings": 0,
            "pending_requests": 0
        }

    if session:
        # Проверяем, является ли пользователь администратором
        result = await session.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        is_admin = user.is_admin if user and hasattr(user, 'is_admin') else False
        
        if is_admin:
            # Получаем статистику для админ-панели
            clients_result = await session.execute(select(User))
            total_clients = len(clients_result.scalars().all())
            
            # Получаем сегодняшние записи
            from datetime import date
            today = date.today()
            bookings_result = await session.execute(
                select(Booking).where(Booking.date == today)
            )
            today_bookings = len(bookings_result.scalars().all())
            
            # Получаем количество неподтвержденных записей
            pending_result = await session.execute(
                select(Booking).where(Booking.confirmed == False)
            )
            pending_requests = len(pending_result.scalars().all())
            
            return {
                "total_clients": total_clients,
                "today_bookings": today_bookings,
                "pending_requests": pending_requests
            }

    # Возврат заглушки, если сессия недоступна или пользователь не админ
    return {
        "total_clients": 0,
        "today_bookings": 0,
        "pending_requests": 0
    }


# Data getter for bookings
async def bookings_getter(dialog_manager: DialogManager, **kwargs):
    session = kwargs.get("session")
    
    if session:
        # Получаем все записи
        result = await session.execute(
            select(Booking)
            .join(User, Booking.user_id == User.id)
            .join(Service, Booking.service_id == Service.id)
            .order_by(Booking.created_at.desc())
        )
        bookings = result.all()
        
        booking_lines = []
        for booking in bookings[:10]:  # Показываем последние 10 записей
            user_name = booking.User.name if hasattr(booking, 'User') and booking.User else "Неизвестный"
            service_name = booking.Service.name if hasattr(booking, 'Service') and booking.Service else "Не указана"
            status = "✅" if booking.Booking.confirmed else "⏳"
            booking_lines.append(
                f"{status} {user_name} - {booking.Booking.date} в {booking.Booking.time} ({service_name})"
            )
        
        return {
            "booking_lines_str": "\n".join(booking_lines) if booking_lines else "Нет записей",
            "total_bookings": len(bookings)
        }

    return {
        "booking_lines_str": "Нет записей",
        "total_bookings": 0
    }


# Callback function to return to admin panel
async def back_to_admin(callback: CallbackQuery, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AdminSG.main)


# Admin dialog
admin_dialog = Dialog(
    Window(
        Format("⚙️ Админ-панель\n\n"
               "📊 Статистика:\n"
               "Всего клиентов: {total_clients}\n"
               "Записей сегодня: {today_bookings}\n"
               "Неподтв. запросов: {pending_requests}\n\n"
               "Выберите действие:"),
        Row(
            Button(Const("📋 Записи"), id="show_bookings_btn", on_click=lambda c, b, m: m.switch_to(AdminSG.show_bookings)),
            Button(Const("👥 Клиенты"), id="show_clients_btn", on_click=lambda c, b, m: m.switch_to(AdminSG.show_clients)),
        ),
        Row(
            Button(Const("📈 Статистика"), id="show_stats_btn", on_click=lambda c, b, m: m.switch_to(AdminSG.show_stats)),
            Button(Const("📤 Рассылка"), id="broadcast_btn", on_click=lambda c, b, m: m.switch_to(AdminSG.broadcast)),
        ),
        Cancel(Const("◀️ Назад")),
        state=AdminSG.main,
        getter=admin_getter,
    ),
    Window(
        Format("📋 Управление записями\n\n"
               "Всего записей: {total_bookings}\n\n"
               "{booking_lines_str}"),
        Button(Const("✏️ Подтвердить запись"), id="confirm_booking"),
        Row(
            Button(Const("⬅️ Назад"), id="back_to_admin", on_click=back_to_admin),
            Button(Const("🗑️ Удалить"), id="delete_booking"),
        ),
        state=AdminSG.show_bookings,
        getter=bookings_getter,
    ),
)
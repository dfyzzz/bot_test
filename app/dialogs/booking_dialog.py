from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Select, Back, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from datetime import datetime, timedelta

router = Router()

# States for booking dialog
from aiogram.fsm.state import State, StatesGroup

class BookingSG(StatesGroup):
    choose_service = State()
    choose_date = State()
    choose_time = State()
    confirm_booking = State()


# Data getters
async def services_getter(dialog_manager: DialogManager, **kwargs):
    # Здесь будет получение списка услуг из базы данных
    # Пока что возвращаем заглушку
    return {
        "services": [
            {"id": 1, "name": "Маникюр", "duration": 60},
            {"id": 2, "name": "Педикюр", "duration": 60},
            {"id": 3, "name": "Комбинированный", "duration": 90}
        ]
    }


async def dates_getter(dialog_manager: DialogManager, **kwargs):
    # Возвращаем ближайшие 7 дней
    dates = []
    for i in range(7):
        date = datetime.now().date() + timedelta(days=i)
        dates.append({"date": date, "formatted": date.strftime("%d.%m.%Y")})
    return {"dates": dates}


async def times_getter(dialog_manager: DialogManager, **kwargs):
    # Получаем доступные слоты времени для выбранной даты
    selected_date_str = dialog_manager.dialog_data.get("selected_date")
    if selected_date_str:
        # Здесь будет получение доступных слотов из базы данных
        # Пока что возвращаем заглушку
        times = ["10:00", "12:00", "14:00", "16:00", "18:00"]
        return {"times": times}
    return {"times": []}


# Callback functions for selection
async def on_service_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    # Сохраняем выбранную услугу
    dialog_manager.dialog_data["selected_service_id"] = int(item_id)
    await dialog_manager.switch_to(BookingSG.choose_date)


async def on_date_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    # Сохраняем выбранную дату
    dialog_manager.dialog_data["selected_date"] = item_id
    await dialog_manager.switch_to(BookingSG.choose_time)


async def on_time_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    # Сохраняем выбранное время
    dialog_manager.dialog_data["selected_time"] = item_id
    await dialog_manager.switch_to(BookingSG.confirm_booking)


async def on_confirm_booking(callback: CallbackQuery, widget, dialog_manager: DialogManager):
    # Подтверждаем бронирование
    # Здесь будет логика сохранения бронирования в базу данных
    await callback.answer("Ваша запись подтверждена!")
    await dialog_manager.done()


# Async getter for confirm window
async def confirm_getter(**kwargs):
    dialog_manager = kwargs.get("dialog_manager")
    if dialog_manager:
        return {
            "date": dialog_manager.dialog_data.get("selected_date", "Не указана"),
            "time": dialog_manager.dialog_data.get("selected_time", "Не указано"),
            "service": "Услуга"
        }
    return {
        "date": "Не указана",
        "time": "Не указано",
        "service": "Услуга"
    }


# Booking dialog
booking_dialog = Dialog(
    Window(
        Const("Выберите услугу:"),
        Select(
            Format("{item[name]}"),
            id="service",
            item_id_getter=lambda x: str(x["id"]),
            items="services",
            on_click=on_service_selected,
        ),
        Cancel(Const("◀️ Назад")),
        state=BookingSG.choose_service,
        getter=services_getter,
    ),
    Window(
        Const("Выберите дату:"),
        Select(
            Format("{item[formatted]}"),
            id="date",
            item_id_getter=lambda x: x["date"].isoformat(),
            items="dates",
            on_click=on_date_selected,
        ),
        Back(Const("◀️ Назад")),
        state=BookingSG.choose_date,
        getter=dates_getter,
    ),
    Window(
        Const("Выберите время:"),
        Select(
            Format("{item}"),
            id="time",
            item_id_getter=lambda x: x,
            items="times",
            on_click=on_time_selected,
        ),
        Back(Const("◀️ Назад")),
        state=BookingSG.choose_time,
        getter=times_getter,
    ),
    Window(
        Format("Подтвердите запись:\n\nДата: {date}\nВремя: {time}\nУслуга: {service}"),
        Row(
            Button(Const("✅ Подтвердить"), id="confirm", on_click=on_confirm_booking),
            Button(Const("❌ Отмена"), id="cancel", on_click=lambda c, b, m: m.done()),
        ),
        Back(Const("◀️ Назад")),
        state=BookingSG.confirm_booking,
        getter=confirm_getter,
    ),
)
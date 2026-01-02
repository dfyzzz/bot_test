from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, date
from datetime import time as dt_time
from typing import List


def get_date_selection_keyboard(dates: List[date]) -> InlineKeyboardMarkup:
    """Keyboard for date selection"""
    builder = InlineKeyboardBuilder()
    
    # Group dates by week
    for date_obj in dates:
        builder.add(InlineKeyboardButton(
            text=date_obj.strftime("%d %b"),
            callback_data=f"date_{date_obj.strftime('%Y-%m-%d')}"
        ))
    
    builder.adjust(3)  # 3 buttons per row
    
    # Add back button
    builder.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_service"
    ))
    
    return builder.as_markup()


def get_time_selection_keyboard(times: List[dt_time], selected_date: date) -> InlineKeyboardMarkup:
    """Keyboard for time selection"""
    builder = InlineKeyboardBuilder()
    
    # Format date for callback
    date_str = selected_date.strftime('%Y-%m-%d')
    
    for time_slot in times:
        builder.add(InlineKeyboardButton(
            text=time_slot.strftime("%H:%M"),
            callback_data=f"time_{date_str}_{time_slot.strftime('%H:%M')}"
        ))
    
    builder.adjust(4)  # 4 buttons per row
    
    # Add back button
    builder.add(InlineKeyboardButton(
        text="🔙 Назад к выбору даты",
        callback_data=f"back_to_date_{date_str}"
    ))
    
    return builder.as_markup()


def get_confirm_booking_keyboard(date: date, time_slot: dt_time, service_name: str) -> InlineKeyboardMarkup:
    """Keyboard for booking confirmation"""
    builder = InlineKeyboardBuilder()
    
    # Format date and time for callback
    date_str = date.strftime('%Y-%m-%d')
    time_str = time_slot.strftime('%H:%M')
    
    builder.add(InlineKeyboardButton(
        text="✅ Подтвердить запись",
        callback_data=f"confirm_{date_str}_{time_str}_{service_name}"
    ))
    
    builder.add(InlineKeyboardButton(
        text="❌ Отмена",
        callback_data="cancel_booking"
    ))
    
    return builder.as_markup()


def get_user_profile_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for user profile"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить профиль", callback_data="refresh_profile"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile"),
    )
    builder.row(
        InlineKeyboardButton(text="📋 История записей", callback_data="view_history"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
    )
    
    return builder.as_markup()


def get_history_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for history view"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="🔙 Назад к профилю",
        callback_data="back_to_profile"
    ))
    builder.add(InlineKeyboardButton(
        text="🏠 Главное меню",
        callback_data="main_menu"
    ))
    
    builder.adjust(2)
    
    return builder.as_markup()

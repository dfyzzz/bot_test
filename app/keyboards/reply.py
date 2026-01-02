from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard(is_admin: bool = False):
    """Main keyboard for users - simplified version for dialogs"""
    builder = InlineKeyboardBuilder()
    
    # Common buttons
    builder.row(
        InlineKeyboardButton(text="📅 Записаться", callback_data="book"),
        InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile"),
    )
    builder.row(
        InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
        InlineKeyboardButton(text="⭐ Оставить отзыв", callback_data="feedback"),
    )
    
    # Admin button if user is admin
    if is_admin:
        builder.row(
            InlineKeyboardButton(text="⚙️ Админ-панель", callback_data="admin_panel"),
        )
    
    return builder.as_markup()


def get_user_profile_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for user profile"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_profile"),
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile"),
    )
    builder.row(
        InlineKeyboardButton(text="📋 История записей", callback_data="view_history"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
    )
    
    return builder.as_markup()

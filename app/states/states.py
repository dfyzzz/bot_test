from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """States for user interactions"""
    waiting_for_contact = State()
    waiting_for_service_selection = State()
    waiting_for_date_selection = State()
    waiting_for_time_selection = State()
    waiting_for_booking_confirmation = State()
    waiting_for_review = State()


class AdminStates(StatesGroup):
    """States for admin interactions"""
    waiting_for_broadcast_message = State()
    waiting_for_export_period = State()
    waiting_for_schedule_settings = State()
    waiting_for_service_management = State()
    waiting_for_notification_settings = State()


class CommonStates(StatesGroup):
    """Common states for both users and admins"""
    waiting_for_main_menu = State()
    waiting_for_profile_update = State()
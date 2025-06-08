from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton(text="➕ Добавить привычку", callback_data="add_habit")],
        [InlineKeyboardButton(text="📋 Мои привычки", callback_data="my_habits")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
  

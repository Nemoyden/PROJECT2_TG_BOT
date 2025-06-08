from aiogram.fsm.state import StatesGroup, State

class AddHabit(StatesGroup):
    waiting_for_habit_name = State()
    waiting_for_time = State()

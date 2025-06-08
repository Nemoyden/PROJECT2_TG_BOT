from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import get_main_menu
from utils.logger import logger
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

router = Router()

@dataclass
class Habit:
    name: str
    notification_time: str = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

# Хранилище привычек (в реальном приложении лучше использовать базу данных)
user_habits: Dict[int, List[Habit]] = {}

class HabitStates(StatesGroup):
    waiting_for_habit_name = State()
    waiting_for_notification_time = State()
    waiting_for_habit_view = State()
    waiting_for_habit_delete = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} начал работу с ботом")
    # Инициализируем список привычек для нового пользователя
    user_habits[message.from_user.id] = []
    await message.answer(
        "Добро пожаловать в Habits Tracker! 🎯\n"
        "Простое и удобное приложение для формирования полезных привычек прямо в Telegram!\n\n"
        "🚀 Как начать?\n"
        "1️⃣ Создайте привычку – придумайте, что хотите делать регулярно, и добавьте в приложение.\n"
        "2️⃣ Настройте уведомления – выберите удобное время, чтобы не забывать про свою цель.\n"
        "3️⃣ Отмечайте выполнение – следите за своим прогрессом и создавайте идеальные серии!\n\n"
        "📋 Доступные команды:\n"
        "/start — начать работу с ботом\n"
        "/help — показать это сообщение\n"
        "/addhabit — добавить новую привычку\n"
        "/myhabits — посмотреть список ваших привычек\n"
        "/deletehabit — удалить привычку\n\n"
        "💡 Совет: Вы также можете использовать кнопки меню для быстрого доступа к основным функциям!",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n\n"
        "📋 <b>Доступные команды:</b>\n"
        "/start — начать работу с ботом\n"
        "/help — показать это сообщение\n"
        "/addhabit — добавить новую привычку\n"
        "/myhabits — посмотреть список ваших привычек\n"
        "/deletehabit — удалить привычку\n\n"
        "💡 <b>Как использовать:</b>\n"
        "1. Добавьте привычку командой /addhabit или через кнопку меню\n"
        "2. Укажите время уведомления в формате ЧЧ:ММ\n"
        "3. Следите за своими привычками через /myhabits\n"
        "4. При необходимости удаляйте привычки через /deletehabit"
    )

@router.message(Command("addhabit"))
async def cmd_add_habit(message: types.Message, state: FSMContext):
    await state.set_state(HabitStates.waiting_for_habit_name)
    await message.answer("Введите название вашей новой привычки:")

@router.callback_query(lambda c: c.data == "add_habit")
async def process_add_habit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(HabitStates.waiting_for_habit_name)
    await callback.message.answer("Введите название вашей новой привычки:")

@router.message(HabitStates.waiting_for_habit_name)
async def process_habit_name(message: types.Message, state: FSMContext):
    habit_name = message.text
    user_id = message.from_user.id
    
    # Создаем новую привычку
    new_habit = Habit(name=habit_name)
    
    # Добавляем привычку в список пользователя
    if user_id not in user_habits:
        user_habits[user_id] = []
    user_habits[user_id].append(new_habit)
    
    # Переходим к установке времени уведомления
    await state.set_state(HabitStates.waiting_for_notification_time)
    await message.answer(
        f"Привычка '{habit_name}' успешно добавлена!\n"
        "Теперь введите время для уведомлений в формате ЧЧ:ММ (например, 09:00):"
    )

@router.message(HabitStates.waiting_for_notification_time)
async def process_notification_time(message: types.Message, state: FSMContext):
    time_str = message.text
    user_id = message.from_user.id
    
    try:
        # Проверяем формат времени
        datetime.strptime(time_str, "%H:%M")
        
        # Устанавливаем время уведомления для последней добавленной привычки
        if user_habits[user_id]:
            user_habits[user_id][-1].notification_time = time_str
            await message.answer(
                f"Время уведомления установлено на {time_str}\n"
                f"Привычка '{user_habits[user_id][-1].name}' полностью настроена!"
            )
    except ValueError:
        await message.answer(
            "Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ (например, 09:00):"
        )
        return
    
    await state.clear()

@router.message(Command("myhabits"))
async def cmd_my_habits(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_habits or not user_habits[user_id]:
        await message.answer("У вас пока нет добавленных привычек.")
        return
    
    habits_list = "\n".join([
        f"{i+1}. {habit.name} (уведомление в {habit.notification_time or 'не установлено'})"
        for i, habit in enumerate(user_habits[user_id])
    ])
    await message.answer(f"Ваши привычки:\n{habits_list}")

@router.callback_query(lambda c: c.data == "my_habits")
async def process_my_habits(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    if user_id not in user_habits or not user_habits[user_id]:
        await callback.message.answer("У вас пока нет добавленных привычек.")
        return
    
    habits_list = "\n".join([
        f"{i+1}. {habit.name} (уведомление в {habit.notification_time or 'не установлено'})"
        for i, habit in enumerate(user_habits[user_id])
    ])
    await callback.message.answer(f"Ваши привычки:\n{habits_list}")

@router.message(Command("deletehabit"))
async def cmd_delete_habit(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_habits or not user_habits[user_id]:
        await message.answer("У вас пока нет добавленных привычек.")
        return
    
    habits_list = "\n".join([
        f"{i+1}. {habit.name}"
        for i, habit in enumerate(user_habits[user_id])
    ])
    await state.set_state(HabitStates.waiting_for_habit_delete)
    await message.answer(
        f"Выберите номер привычки для удаления:\n{habits_list}"
    )

@router.message(HabitStates.waiting_for_habit_delete)
async def process_habit_delete(message: types.Message, state: FSMContext):
    try:
        habit_index = int(message.text) - 1
        user_id = message.from_user.id
        
        if 0 <= habit_index < len(user_habits[user_id]):
            deleted_habit = user_habits[user_id].pop(habit_index)
            await message.answer(f"Привычка '{deleted_habit.name}' успешно удалена!")
        else:
            await message.answer("Неверный номер привычки. Пожалуйста, выберите номер из списка.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите номер привычки цифрами.")
        return
    
    await state.clear()

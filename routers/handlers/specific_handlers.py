from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states import AddHabit
from keyboards.inline import get_main_menu
from services.storage_service import load_habits, save_habits
from services.api_client import get_quote
from utils.logger import logger

router = Router()

@router.message(F.text == "➕ Добавить привычку")
@router.message(F.text == "/addhabit")
async def add_habit_start(message: types.Message, state: FSMContext):
    await message.answer("Введите название новой привычки:")
    await state.set_state(AddHabit.waiting_for_habit_name)


@router.message(AddHabit.waiting_for_habit_name)
async def add_habit_name(message: types.Message, state: FSMContext):
    habit_name = message.text.strip()
    await state.update_data(habit_name=habit_name)
    await message.answer("Во сколько часов напоминать? (например, 09:00)")
    await state.set_state(AddHabit.waiting_for_time)

@router.message(AddHabit.waiting_for_time)
async def add_habit_time(message: types.Message, state: FSMContext):
    time = message.text.strip()
    data = await state.get_data()
    habit_name = data["habit_name"]
    user_id = str(message.from_user.id)
    habits = load_habits()
    if user_id not in habits:
        habits[user_id] = []
    habits[user_id].append({
        "name": habit_name,
        "time": time,
        "progress": [],
        "streak": 0
    })
    save_habits(habits)
    await message.answer(f"Привычка <b>{habit_name}</b> добавлена! ⏰ Время напоминания: {time}", reply_markup=get_main_menu())
    logger.info(f"Пользователь {user_id} добавил привычку: {habit_name} в {time}")
    await state.clear()

@router.message(F.text == "📋 Мои привычки")
@router.message(F.text == "/myhabits")
async def my_habits(message: types.Message):
    user_id = str(message.from_user.id)
    habits = load_habits()
    user_habits = habits.get(user_id, [])
    if not user_habits:
        await message.answer("У вас пока нет привычек. Добавьте первую!")
        return
    text = "Ваши привычки:\n"
    for idx, habit in enumerate(user_habits, 1):
        text += f"{idx}. {habit['name']} (⏰ {habit['time']})\n"
    await message.answer(text)

@router.message(F.text == "📊 Статистика")
@router.message(F.text == "/stats")
async def stats(message: types.Message):
    user_id = str(message.from_user.id)
    habits = load_habits()
    user_habits = habits.get(user_id, [])
    if not user_habits:
        await message.answer("У вас пока нет привычек.")
        return
    text = "📊 <b>Ваша статистика:</b>\n"
    for habit in user_habits:
        streak = habit.get("streak", 0)
        text += f"• {habit['name']}: серия {streak} дней\n"
    quote = await get_quote()
    if quote:
        text += f"\n💡 Мотивация: <i>{quote['content']}</i> — {quote['author']}"
    await message.answer(text)

@router.message(F.text == "/deletehabit")
async def delete_habit(message: types.Message):
    user_id = str(message.from_user.id)
    habits = load_habits()
    user_habits = habits.get(user_id, [])
    if not user_habits:
        await message.answer("У вас нет привычек для удаления.")
        return
    text = "Введите номер привычки для удаления:\n"
    for idx, habit in enumerate(user_habits, 1):
        text += f"{idx}. {habit['name']} (⏰ {habit['time']})\n"
    await message.answer(text)
   
    from aiogram.fsm.context import FSMContext
    from states import DeleteHabit
    await FSMContext.set_state(DeleteHabit.waiting_for_habit_number)

from aiogram.fsm.state import State, StatesGroup

class DeleteHabit(StatesGroup):
    waiting_for_habit_number = State()

@router.message(DeleteHabit.waiting_for_habit_number)
async def process_delete_habit(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    habits = load_habits()
    user_habits = habits.get(user_id, [])
    try:
        idx = int(message.text.strip()) - 1
        if idx < 0 or idx >= len(user_habits):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректный номер привычки.")
        return
    removed = user_habits.pop(idx)
    habits[user_id] = user_habits
    save_habits(habits)
    await message.answer(f"Привычка <b>{removed['name']}</b> удалена.", reply_markup=get_main_menu())
    logger.info(f"Пользователь {user_id} удалил привычку: {removed['name']}")
    await state.clear()


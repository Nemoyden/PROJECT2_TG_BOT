from aiogram import Router, types
from aiogram.filters import Command
from keyboards.inline import get_main_menu
from utils.logger import logger

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} начал работу с ботом")
    await message.answer(
        "Добро пожаловать в Habits Tracker! 🎯\n"
        "Простое и удобное приложение для формирования полезных привычек прямо в Telegram!\n\n"
        "🚀 Как начать?\n"
        "1️⃣ Создайте привычку – придумайте, что хотите делать регулярно, и добавьте в приложение.\n"
        "2️⃣ Настройте уведомления – выберите удобное время, чтобы не забывать про свою цель.\n"
        "3️⃣ Отмечайте выполнение – следите за своим прогрессом и создавайте идеальные серии!\n",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n"
        "/start — начать работу\n"
        "/addhabit — добавить привычку\n"
        "/myhabits — мои привычки\n"
        "/stats — статистика\n"
        "/deletehabit — удалить привычку\n"
        "/help — помощь"
    )

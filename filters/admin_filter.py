from aiogram.filters import BaseFilter
from aiogram.types import Message

ADMINS = [123456789]  # Замените на свой user_id

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS

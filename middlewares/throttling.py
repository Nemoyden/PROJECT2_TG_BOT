from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
import asyncio

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1.0):
        self.rate_limit = rate_limit
        self.users = {}

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        if user_id in self.users:
            await asyncio.sleep(self.rate_limit)
        self.users[user_id] = True
        return await handler(event, data)

import aiohttp
from utils.logger import logger

api_cache = {}

async def get_quote():
    url = "https://api.quotable.io/random"
    if url in api_cache:
        return api_cache[url]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                data = await resp.json()
                api_cache[url] = data
                return data
    except Exception as e:
        logger.error(f"Ошибка при обращении к API: {e}")
        return None

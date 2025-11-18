import aiohttp
from typing import Dict, Any

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Асинхронный HTTP-запрос для получения JSON"""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()
import aiohttp
from typing import List, Dict

USERS_DATA_URL = 'https://jsonplaceholder.typicode.com/users'
POSTS_DATA_URL = 'https://jsonplaceholder.typicode.com/posts'


async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    connector = aiohttp.TCPConnector(ssl=False)  # Отключаем проверку SSL
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def fetch_users_data(session: aiohttp.ClientSession) -> List[Dict]:
    return await fetch_json(session, USERS_DATA_URL)


async def fetch_posts_data(session: aiohttp.ClientSession) -> List[Dict]:
    return await fetch_json(session, POSTS_DATA_URL)
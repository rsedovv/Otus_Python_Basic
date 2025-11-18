import asyncio
import aiohttp
from jsonplaceholder_requests import fetch_json

async def main():
    async with aiohttp.ClientSession() as http_session:
        users, posts = await asyncio.gather(
            fetch_json(http_session, 'https://jsonplaceholder.typicode.com/users'),
            fetch_json(http_session, 'https://jsonplaceholder.typicode.com/posts')
        )
        print(f"Получено пользователей: {len(users)}, постов: {len(posts)}")

if __name__ == '__main__':
    asyncio.run(main())
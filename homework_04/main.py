import asyncio
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post

DATABASE_URL = "sqlite+aiosqlite:///database.sqlite"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url, ssl=False) as response:
        response.raise_for_status()
        return await response.json()


async def create_users(session: AsyncSession, users_data: list[dict]):
    valid_user_fields = {'id', 'name', 'username', 'email'}
    filtered_users = [{k: v for k, v in u.items() if k in valid_user_fields} for u in users_data]

    users = [User(**user_data) for user_data in filtered_users]
    session.add_all(users)
    await session.commit()
    print(f"Создано пользователей: {len(users)}")


async def create_posts(session: AsyncSession, posts_data: list[dict]):
    valid_post_fields = {'id', 'title', 'body', 'userId'}
    transformed_posts = []

    for post in posts_data:
        p = {k: v for k, v in post.items() if k in valid_post_fields}
        p['user_id'] = p.pop('userId', None)
        transformed_posts.append(p)

    posts = [Post(**post_data) for post_data in transformed_posts]
    session.add_all(posts)
    await session.commit()
    print(f"Создано постов: {len(posts)}")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with aiohttp.ClientSession() as http_session:
        users_data = await fetch_json(http_session, 'https://jsonplaceholder.typicode.com/users')
        posts_data = await fetch_json(http_session, 'https://jsonplaceholder.typicode.com/posts')

    async with AsyncSessionLocal() as db_session:
        await create_users(db_session, users_data)
        await create_posts(db_session, posts_data)

        users = (await db_session.execute(select(User))).scalars().all()
        print("\nПример данных пользователей:")
        for user in users[:3]:
            print(f"User {user.id}: {user.name} ({user.email})")

        posts = (await db_session.execute(select(Post))).scalars().all()
        print("\nПример данных постов:")
        for post in posts[:3]:
            print(f"Post {post.id}: {post.title[:20]}...")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
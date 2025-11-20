import asyncio
import aiohttp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.sql.expression import text
from models import Base, User, Post
from jsonplaceholder_requests import fetch_json

DATABASE_URL = "sqlite+aiosqlite:///blog.db"


async def ensure_tables_exist():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_to_db(users_data, posts_data):
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM posts"))
        await conn.execute(text("DELETE FROM users"))

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        users = []
        for data in users_data:
            user = User(name=data['name'], username=data['username'], email=data['email'])
            users.append(user)

        session.add_all(users)

        posts = []
        for post_data in posts_data:
            post = Post(title=post_data['title'], body=post_data['body'], user_id=post_data['userId'])
            posts.append(post)

        session.add_all(posts)

        await session.commit()


async def select_and_print_data():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        result_users = await session.execute(select(User))
        users = result_users.scalars().all()

        result_posts = await session.execute(select(Post))
        posts = result_posts.scalars().all()

        print("\nПользователи:")
        for user in users:
            print(f"ID: {user.id}, Имя: {user.name}, Username: {user.username}, Email: {user.email}")

        print("\nСообщения:")
        for post in posts:
            print(f"ID поста: {post.id}, Название: {post.title[:20]}... , Автор ID: {post.user_id}")


async def main():
    # Предварительное создание таблиц
    await ensure_tables_exist()

    async with aiohttp.ClientSession() as http_session:
        users, posts = await asyncio.gather(
            fetch_json(http_session, 'https://jsonplaceholder.typicode.com/users'),
            fetch_json(http_session, 'https://jsonplaceholder.typicode.com/posts')
        )
        print(f"\nПолучено пользователей: {len(users)}, сообщений: {len(posts)}\n")
        await save_to_db(users, posts)
        await select_and_print_data()  # Читаем и выводим данные


if __name__ == '__main__':
    asyncio.run(main())
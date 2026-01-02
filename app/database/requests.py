from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, BigInteger, select
from .models import Base, User
from typing import AsyncGenerator


async def create_sessionmaker(database_url: str) -> async_sessionmaker:
    """Create an async sessionmaker for database operations"""
    engine = create_async_engine(database_url)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create and return async sessionmaker
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return async_session


async def get_db_session(async_session: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection"""
    async with async_session() as session:
        yield session


async def get_or_create_user(session: AsyncSession, telegram_id: int, first_name: str | None = None, username: str | None = None):
    """Get existing user or create new one"""
    try:
        # Try to get existing user
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                telegram_id=telegram_id,
                name=first_name or username or "Пользователь",
                is_active=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        elif user.name != (first_name or username or "Пользователь"):
            # Update user's name if it has changed
            user.name = first_name or username or "Пользователь"
            await session.commit()
        
        return user
    except Exception as e:
        # Rollback in case of error
        await session.rollback()
        # Try again to get the user (in case of concurrent creation)
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user
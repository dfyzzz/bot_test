import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from app.config import Settings
from app.database import create_sessionmaker
from app.middlewares.db_session import DbSessionMiddleware
from app.handlers import admin, user, booking, common
from app.services.scheduler import init_scheduler
from aiogram_dialog import setup_dialogs


async def main():
    # Load settings
    settings = Settings()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Initialize bot
    bot = Bot(token=settings.bot_token.get_secret_value())
    
    # Initialize Redis storage for FSM
    from aiogram.fsm.storage.base import DefaultKeyBuilder
    storage = RedisStorage.from_url(
        settings.redis_url,
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    
    # Initialize dispatcher
    dp = Dispatcher(storage=storage)
    
    # Create database sessionmaker
    sessionmaker = await create_sessionmaker(settings.database_url)
    
    # Initialize scheduler
    scheduler = await init_scheduler(settings, sessionmaker)
    
    # Setup dialogs before registering middlewares
    from app.dialogs.main_menu import main_menu_dialog
    from app.dialogs.booking_dialog import booking_dialog
    from app.dialogs.profile_dialog import profile_dialog
    from app.dialogs.admin_dialog import admin_dialog
    dp.include_router(main_menu_dialog)
    dp.include_router(booking_dialog)
    dp.include_router(profile_dialog)
    dp.include_router(admin_dialog)
    
    # Register middlewares
    dp.message.middleware(DbSessionMiddleware(sessionmaker))
    dp.callback_query.middleware(DbSessionMiddleware(sessionmaker))
    
    # Include routers
    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(booking.router)
    dp.include_router(common.router)
    
    # Setup dialogs
    from aiogram_dialog import setup_dialogs
    setup_dialogs(dp)
    
    # Start scheduler
    scheduler.start()
    
    logger.info("Bot is starting...")
    
    # Start polling
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        await bot.session.close()
        if hasattr(sessionmaker, 'close'):
            await sessionmaker.close()
        if scheduler.running:
            scheduler.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
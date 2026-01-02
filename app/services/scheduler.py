from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from app.config import Settings
from sqlalchemy.ext.asyncio import async_sessionmaker
import logging


async def init_scheduler(settings: Settings, sessionmaker: async_sessionmaker):
    """Initialize the scheduler with necessary jobs"""
    # Configure jobstore and executor
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': AsyncIOExecutor()
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    
    # Create scheduler
    scheduler = AsyncIOScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
    )
    
    # Add your scheduled jobs here
    # Example: scheduler.add_job(your_function, 'interval', minutes=30)
    
    return scheduler
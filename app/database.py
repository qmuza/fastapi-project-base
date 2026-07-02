from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings
from app.logger import get_logger

_logger = get_logger(__name__)

engine = create_async_engine(
    settings.get_database_url(),
    echo=False, # We already set up a logger so turn off the default one
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@event.listens_for(AsyncSessionLocal, "after_commit")
def _log_commit(session):
    _logger.info("DB COMMIT")
@event.listens_for(AsyncSessionLocal, "after_rollback")
def _log_rollback(session):
    _logger.info("DB ROLLBACK")
@event.listens_for(AsyncSessionLocal, "after_begin")
def _log_begin(session, transaction, connection):
    _logger.info("DB BEGIN")

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

# Engine erstellen
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

# Session-Maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base für Modelle
Base = declarative_base()


async def get_db():
    """Dependency für FastAPI"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Datenbank initialisieren"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

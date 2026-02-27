from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

raw_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/giftforge")

# Railway and other providers often supply a URL starting with "postgres://".
# SQLAlchemy treats that as the psycopg2 driver, which isn't installed in our
# image.  Convert to the asyncpg scheme automatically so we don't need
# to rely on the exact format coming from the environment.
if raw_url.startswith("postgres://"):
    # postgres://user:pass@host/db -> postgresql+asyncpg://user:pass@host/db
    DATABASE_URL = "postgresql+asyncpg://" + raw_url[len("postgres://"):]
else:
    DATABASE_URL = raw_url

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

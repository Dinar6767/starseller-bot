from sqlalchemy import BigInteger, Boolean, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timezone
import os

# --- УМНЫЙ ПУТЬ К БАЗЕ ДАННЫХ ---
# Если переменная DB_PATH задана (например, ботом), используем её.
# Иначе используем локальный файл db.sqlite3.
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

# Формируем правильную строку подключения для SQLAlchemy
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Создаём движок с правильным путём
engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(64))
    chat_id = mapped_column(BigInteger)
    amount: Mapped[int] = mapped_column()
    username: Mapped[str] = mapped_column(String(32))
    purchase_method: Mapped[str] = mapped_column(String(3))
    is_accepted: Mapped[str] = mapped_column(String(5))
    payment_status: Mapped[str] = mapped_column(String(9))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
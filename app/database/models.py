from sqlalchemy import BigInteger, Boolean, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timezone
import os

# --- УМНЫЙ ПУТЬ К БАЗЕ ДАННЫХ ---
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

# --- ГАРАНТИРОВАННОЕ СОЗДАНИЕ ФАЙЛА БАЗЫ (чтобы Railway не падал) ---
# Если файла нет, создаём его принудительно (это даст права на запись)
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    try:
        os.makedirs(db_dir, exist_ok=True)
        print(f"✅ Создана папка для базы: {db_dir}")
    except:
        pass

if not os.path.exists(DB_PATH):
    try:
        with open(DB_PATH, 'w') as f:
            f.write('')  # Создаём пустой файл
        print(f"✅ Файл базы данных создан: {DB_PATH}")
    except Exception as e:
        print(f"⚠️ Не удалось создать файл базы: {e}")

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
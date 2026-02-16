import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker,Session
from loguru import logger
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / "DB/.env"
load_dotenv(env_path)

DB_Host = os.getenv("DB_HOST")
DB_User = os.getenv("DB_USER")
DB_Password = os.getenv("DB_PASSWORLD")
DB_Name = os.getenv("DB_NAME")
DB_Port = os.getenv("DB_PORT")

logger.info("Загрузка конфигурации базы данных из .env")

logger.debug(
    "DB Config: host={}, port={}, user={}, name={}",
    DB_Host,
    DB_Port,
    DB_User,
    DB_Name
)

url = f"postgresql+psycopg2://{DB_User}:{DB_Password}@{DB_Host}:{DB_Port}/{DB_Name}"
logger.info("Создание SQLAlchemy engine")
engine = create_engine(
    url,
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30
)
logger.success("Engine успешно создан")

SessionDB = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

logger.success("Sessionmaker успешно настроен")

def GetBD():
    logger.debug("Открытие новой DB-сессии")
    db = SessionDB()
    try:
        yield db
    finally:
        db.close()
        logger.debug("DB-сессия закрыта")
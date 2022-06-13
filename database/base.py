import logging
import os

from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.objects import DatabaseConsts
from utils.logger import debugger

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)


DATABASE_URL = 'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}'.format(
    user=DatabaseConsts.MYSQL_USER,
    password=DatabaseConsts.MYSQL_PASSWORD,
    host=DatabaseConsts.MYSQL_HOST,
    port=DatabaseConsts.MYSQL_PORT,
    database=DatabaseConsts.MYSQL_DATABASE,
)


class AsyncDatabaseSession(object):
    def __init__(self):
        self._session = None
        self._engine = None
        self.init()

    def __getattr__(self, name):
        return getattr(self._session, name)

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    def init(self):
        self._engine = create_async_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_size=DatabaseConsts.SA_POOL_SIZE,
            pool_recycle=DatabaseConsts.SA_POOL_RECYCLE,
            pool_timeout=DatabaseConsts.SA_POOL_TIMEOUT,
            max_overflow=DatabaseConsts.SA_POOL_MAX_OVERFLOW,
            connect_args={
                'server_settings': {
                    'application_name': self.application_name,
                    'options': '-c statement_timeout={}'.format(DatabaseConsts.MYSQL_TIMEOUT_MS)
                },
            }
        )

        self._session = sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)

        @event.listens_for(self._engine.sync_engine, "connect")
        def connect(dbapi_connection, connection_record):
            debugger.debug('engine connect')
            connection_record.info['pid'] = os.getpid()

        @event.listens_for(self._engine.sync_engine, "checkout")
        def checkout(dbapi_connection, connection_record, connection_proxy):
            debugger.debug('engine checkout')

            pid = os.getpid()

            if connection_record.info['pid'] != pid:
                connection_record.dbapi_connection = connection_proxy.dbapi_connection = None
                raise exc.DisconnectionError(
                    "Connection record belongs to pid %s, "
                    "attempting to check out in pid %s" %
                    (connection_record.info['pid'], pid)
                )


# AsyncDatabaseSession for getting engine & session
async_db_session = AsyncDatabaseSession()
async_session = async_db_session.session  # get session
engine = async_db_session.engine  # get engine

Base = declarative_base(metadata=MetaData(schema=DatabaseConsts.MYSQL_SCHEMA))


# Fastapi Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

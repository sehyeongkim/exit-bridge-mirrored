from fastapi import FastAPI, Depends
from utils.logger import debugger, init_logger
from app.config import config_obj
from database.base import engine, get_session, AsyncSession
from database.service import UserService


app = FastAPI()


@app.on_event('startup')
async def startup():
    init_logger(config_obj, 'app.log')
    debugger.info('Starting up...')

    # https://docs.sqlalchemy.org/en/14/core/pooling.html?highlight=connection%20pool#using-connection-pools-with-multiprocessing-or-os-fork
    # to prevent sharing the pooled connections across forked process when using many uvicorn workers
    await engine.dispose()
    debugger.debug('engine has been disposed')


@app.on_event('shutdown')
async def shutdown_event():
    debugger.info('Shutting down...')


@app.get('/hello')
async def hello(user_id, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_user(user_id)
    return {'result': f'hello {user.email}'}

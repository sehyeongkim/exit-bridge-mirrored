from fastapi import FastAPI
from utils.logger import debugger, init_logger
from app.config import config_obj


app = FastAPI()


@app.on_event('startup')
async def startup():
    init_logger(config_obj, 'app.log')
    debugger.info('Starting up...')


@app.on_event('shutdown')
async def shutdown_event():
    debugger.info('Shutting down...')


@app.get('/hello')
async def hello():
    return {'hello': True}

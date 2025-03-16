from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import conf, models, database


models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if conf.DEVMODE:
        models.Base.metadata.drop_all(bind=database.engine)

app = FastAPI(
    lifespan=lifespan,
    root_path=conf.URLPREFIX
)


@app.get('/info', include_in_schema=False)
async def get_info():
    return {'message': 'Hello, World!'}


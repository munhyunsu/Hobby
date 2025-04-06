from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from . import conf, models, database
from . import (
    user_manager,
    token_manager,
)


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_manager.router)
app.include_router(token_manager.router)


@app.get('/info', include_in_schema=False)
async def get_info():
    return {'message': 'Hello, World!'}


import os
import importlib

from typing import Union

from contextlib import asynccontextmanager
from fastapi import FastAPI

ENABLE_GREETERS = ['english', 'korean', 'japanese', 'unknown']


def load_greeters(modules):
    greeters = {}
    for module in modules:
        name = f'greeter.{module}'
        if importlib.util.find_spec(name) is not None:
            mod = importlib.import_module(name)
            greeters[module] = getattr(mod, 'print_hello')


    print(greeters)
    return greeters


greeters = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global greeters
    # Startup codes
    greeters = load_greeters(ENABLE_GREETERS)
    yield
    # Shutdown codes

app = FastAPI(lifespan=lifespan)


@app.get('/')
async def get_index():
    return {'Message': 'Hello, World!'}


@app.get('/greeters')
async def get_greeters():
    return {'Greeters': list(greeters.keys())}


@app.get('/greeter/{module}')
async def get_greeter(module: str):
    if module in greeters.keys():
        return {'Message': greeters[module]()}
    else:
        return {'Message': 'Can not found'}


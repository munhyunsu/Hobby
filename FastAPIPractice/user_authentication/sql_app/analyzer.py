import os
import importlib

from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import models
from .database import engine
from .conf import ENABLE_OPS


ops = {}


def load_ops(modules):
    for module in modules:
        name = f'.{module}'
        if importlib.util.find_spec(name, '.sql_app') is not None:
            mod = importlib.import_module(name, '.sql_app')
            module = module.lower()
            ops[module] = getattr(mod, 'do')

    return ops


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup codes
    ops = load_ops(ENABLE_OPS)
    yield
    # Shutdown codes
    models.Base.metadata.drop_all(bind=engine)

